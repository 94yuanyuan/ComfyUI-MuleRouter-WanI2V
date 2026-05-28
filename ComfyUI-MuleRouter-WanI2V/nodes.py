import requests, json, time, os, base64, io
from PIL import Image
import numpy as np
import torch
import torchaudio
import comfy.utils

class MuleRouterWanI2VNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mode": (["Generate_New", "Recover_Task"], {"default": "Generate_New"}),
                "api_key": ("STRING", {"default": "", "multiline": False}),
                "force_task_id": ("STRING", {"default": ""}),
                "image": ("IMAGE",),
                "prompt": ("STRING", {"multiline": True, "default": ""}),
                "negative_prompt": ("STRING", {"multiline": True, "default": ""}),
                "resolution": (["720p", "1080p"], {"default": "720p"}),
                "duration": (["5", "10", "15"], {"default": "5"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2147483647}),
                "enable_audio": ("BOOLEAN", {"default": True}),
                "prompt_enhancement": ("BOOLEAN", {"default": True}),
                "watermark": ("BOOLEAN", {"default": False}),
                "shot_type": (["single", "multi"], {"default": "single"}),
                "save_dir": ("STRING", {"default": "ComfyUI/output/mulerouter_videos"}),
            },
            "optional": {
                "image_last": ("IMAGE",),
                "audio": ("AUDIO",),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("VIDEO_PATH", "TASK_ID", "VIDEO_URL") 
    FUNCTION = "generate_video"
    CATEGORY = "MuleRouter"

    def _handle_api_error(self, resp):
        """解析 API 錯誤並拋出詳細資訊"""
        try:
            error_data = resp.json().get("error", {})
            code = error_data.get("code", "unknown_error")
            message = error_data.get("message", resp.text)
            return f"API 錯誤 [{code}]: {message}"
        except:
            return f"API 請求失敗，狀態碼: {resp.status_code}, 內容: {resp.text}"

    def _tensor_to_b64(self, tensor):
        """優化：將 Tensor 轉換為 Base64 字串的輔助方法"""
        img_np = (255. * tensor.cpu().numpy()).astype(np.uint8)
        img = Image.fromarray(img_np)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode('utf-8')}"

    def generate_video(self, mode, api_key, force_task_id, image, prompt, negative_prompt, resolution, duration, seed, enable_audio, prompt_enhancement, watermark, shot_type, save_dir, image_last=None, audio=None):
        generation_url = "https://api.mulerouter.ai/vendors/carrothub/v1/wan2.7-i2v-spicy/generation"
        # 關閉 Keep-Alive，避免大檔案 Base64 傳輸時發生 SSLWantWriteError
        headers = {
            "Authorization": f"Bearer {api_key.strip()}", 
            "Content-Type": "application/json",
            "Connection": "close"
        }
        
        # 針對大檔案上傳與輪詢設置不同的 timeout
        post_timeout = 120
        poll_timeout = 30
        task_id = None
        
        if mode == "Recover_Task":
            task_id = force_task_id.strip()
        else:
            if audio is not None:
                enable_audio = False

            # 移除多圖迴圈處理邏輯，僅提取第一張圖片進行 Base64 編碼
            image_b64 = self._tensor_to_b64(image[0])
            
            payload = {
                "prompt": prompt.replace('\n', ' '), 
                "negative_prompt": negative_prompt.replace('\n', ' '),
                "image": image_b64,
                "resolution": resolution,
                "duration": int(duration),
                "seed": seed % 2147483647,
                "enable_audio": enable_audio,
                "prompt_enhancement": prompt_enhancement,
                "watermark": watermark,
                "shot_type": shot_type,
                "safety_check": False
            }
            
            if image_last is not None:
                payload["last_frame"] = self._tensor_to_b64(image_last[0])
            
            if audio is not None:
                try:
                    waveform = audio.get("waveform")
                    sample_rate = audio.get("sample_rate")
                    
                    if waveform is not None and sample_rate is not None:
                        if waveform.dim() == 3:
                            waveform = waveform.squeeze(0)
                            
                        buffered_audio = io.BytesIO()
                        torchaudio.save(buffered_audio, waveform, sample_rate, format="wav")
                        audio_b64 = base64.b64encode(buffered_audio.getvalue()).decode("utf-8")
                        payload["audio"] = f"data:audio/wav;base64,{audio_b64}"
                except Exception as e:
                    raise Exception(f"處理音頻時發生錯誤: {str(e)}")

            resp = requests.post(generation_url, headers=headers, json=payload, timeout=post_timeout)
            if resp.status_code != 200:
                raise Exception(self._handle_api_error(resp))
            
            res_json = resp.json()
            task_id = res_json.get("task_info", {}).get("id") or res_json.get("id")
            print(f"任務建立成功: {task_id}", flush=True)

        status_url = f"{generation_url}/{task_id}"
        max_retries = 200
        
        # 初始化 ComfyUI 的綠色進度條
        pbar = comfy.utils.ProgressBar(max_retries)
        video_url = None
        
        for i in range(max_retries):
            time.sleep(5)
            res = requests.get(status_url, headers=headers, timeout=poll_timeout)
            if res.status_code == 200:
                data = res.json()
                status = data.get("task_info", {}).get("status") or data.get("status", "unknown")
                
                # 每次輪詢觸發一次更新，前台進度條會逐步增加
                pbar.update(1)
                
                if status == "completed":
                    videos = data.get("videos")
                    if videos and len(videos) > 0:
                        video_url = videos[0]
                    else:
                        video_url = data.get("video_url")
                    break
                elif status == "failed":
                    err = data.get("error", data)
                    raise Exception(f"任務執行失敗: {err}")
            else:
                print(f"輪詢中... 狀態碼: {res.status_code}", flush=True)
        
        if not video_url: raise Exception("輪詢任務超時")
        
        if not os.path.exists(save_dir): os.makedirs(save_dir)
        local_path = os.path.join(save_dir, f"video_{task_id}.mp4")
        with requests.get(video_url, stream=True, timeout=post_timeout) as r:
            r.raise_for_status()
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
                
        return (local_path, task_id, video_url)