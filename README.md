# ComfyUI MuleRouter Wan I2V Node

A custom node specifically written for the wan2.7-i2v-spicy API, designed for use in ComfyUI.
這是一個非官方的 ComfyUI 自定義節點，允許你透過 [MuleRouter API](https://www.mulerouter.ai/) 呼叫 Alibaba 的 **Wan 2.7 I2V (Spicy)** 模型，進行圖片生成影片 (Image-to-Video) 的任務。

## 🌟 功能介紹 (Features)

本節點提供以下核心能力：

* **單圖生成影片 (Image to Video)**：輸入單張圖片即可生成高品質動態影片。
* **歷史任務找回 (Recover Task)**：支援透過 Task ID 呼叫並下載過去已完成的影片。
* **Batch 影像支援**：支援 ComfyUI 內建 Batch 影像輸入與自動 Base64 轉檔。
* **完美融合 UI**：原生支援 ComfyUI 綠色進度條 (Progress Bar) 顯示。
* **穩定連線**：針對大檔案傳輸進行連線最佳化 (停用 Keep-Alive) 與防呆保護。

## ⚙️ 核心參數與 API 支援現況說明

本節點的核心參數設置是基於官方 [Wan 2.6 Image-To-Video 文件](https://www.mulerouter.ai/docs/api-reference/endpoint/alibaba/wan2.6-i2v/generation) 所設計。

⚠️ **重要提示 (截至 2026/05/28)**：
目前官方尚未發布 Wan 2.7 的正式文件，且本節點使用的端點為無審查的特化版 (`wan2.7-i2v-spicy`)。

為了避免使用者混淆，**尚未能使用的預留參數，在節點介面上已打上驚嘆號圖標 (❗️) 並做隱藏處理以示提醒**。這些進階功能參數包含：

* `❗️image_last` (首尾幀控制)
* `❗️audio` (自訂音頻，對口型)
* `❗️enable_audio` (開關聲音生成，默認打開無法關閉)
* `❗️prompt_enhancement` (提示詞優化)
* `❗️watermark` (開關浮水印，默認關閉無法打開)
* `❗️shot_type` (單鏡頭/多鏡頭，默認單鏡頭無法更動)

**在官方正式更新模型與解鎖限制之前，傳遞上述參數至 API 接收方皆為「無效參數」**（不會報錯，但也不會有實質效果）。我們保留這些輸入點並將其標記/隱藏，是為了確保未來官方更新 API 功能時，你的工作流可能在第一時間無縫受惠，不需重新連線或大幅更新節點代碼。

## 🧩 推薦基礎工作流 (Recommended Workflow)

要讓這個節點順利運作，推薦在 ComfyUI 中使用以下的基礎節點連接方式：

1. **輸入影像**: 新增一個 `Load Image` (載入影像) 節點，將其 `IMAGE` 輸出端連接到此節點的 `image` 輸入端。
2. **輸入提示詞**: 在此節點的 `prompt` (正向提示詞) 與 `negative_prompt` (負向提示詞) 欄位填寫你想要的畫面描述。
3. **輸入音頻**: 若想加入背景音，新增 `Load Audio` 節點，將其 `AUDIO` 輸出端連接到此節點左側的 `audio` 接入點。
4. **輸出預覽**: 此節點生成完畢後，會自動將影片 mp4 檔案存至 `ComfyUI/output/mulerouter_videos` 目錄下。你也可以將此節點輸出的 `VIDEO_PATH` (字串) 連接給外部的預覽節點或直接到資料夾查看。

## 📝 參數模式說明 (Usage)

* **api_key**: 請填入你在 MuleRouter 取得的 API Key。

* **mode**:

  * `Generate_New`: 建立新影片生成任務。

  * `Recover_Task`: 找回並下載之前的任務（必須在 `force_task_id` 填入欲找回的 Task ID）。

## 🔗 參考工作流 (Example Workflow)

如果你不知道如何開始連接節點，可以直接下載並參考我準備的基礎工作流：

👉 點此下載基礎工作流 [MuleRouter I2V (Wan2.7).json](https://github.com/94yuanyuan/ComfyUI-MuleRouter-WanI2V/blob/main/MuleRouter%20I2V%20(Wan2.7).json)

## 🛠️ 安裝方法與路徑 (Installation)

請確保將本專案的檔案放置於 ComfyUI 的 `custom_nodes` 資料夾中。正確的擺放路徑結構如下：

```text
📂 ComfyUI/
├── 📂 custom_nodes/
│   └── 📂 ComfyUI-MuleRouter-WanI2V/  <-- (本專案資料夾)
│       ├── 📄 __init__.py
│       ├── 📄 nodes.py
│       └── 📄 README.md
└── 📂 user/
    └── 📂 default/
        └── 📂 workflows/
            └── 📄 MuleRouter I2V (Wan2.7)
