ComfyUI MuleRouter Wan I2V Node

A custom node specifically written for the wan2.7-i2v-spicy API, designed for use in ComfyUI.
這是一個非官方的 ComfyUI 自定義節點，允許你透過 MuleRouter API 呼叫 Alibaba 的 Wan 2.7 I2V (Spicy) 模型，進行圖片生成影片 (Image-to-Video) 的任務。

🌟 功能特色 (Features)

支援單圖轉影片 (Image to Video)

支援 ComfyUI 內建 Batch 影像輸入與自動 Base64 轉檔

支援斷點續傳 (Recover Task) 機制，不怕網路中斷

原生支援 ComfyUI 綠色進度條 (Progress Bar) 顯示

針對大檔案傳輸進行連線最佳化 (停用 Keep-Alive) 與防呆保護

預留擴展接口 (支援未來官方解鎖 Audio、Watermark、Last Frame 等功能)

🛠️ 安裝方法 (Installation)

方法一：透過 Git 安裝 (推薦 / Recommended)

打開你的終端機 (Terminal) 或命令提示字元 (CMD)

進入你的 ComfyUI 自定義節點資料夾：

cd ComfyUI/custom_nodes/


複製此專案：

git clone <你的GitHub專案網址>


重新啟動 ComfyUI。

方法二：手動下載 (Manual Download)

點擊頁面右上角的 Code 按鈕 (綠色)，選擇 Download ZIP。

將下載的壓縮檔解壓縮。

將解壓縮出來的整個資料夾（裡面包含 __init__.py 與 nodes.py）放進 ComfyUI/custom_nodes/ 目錄下。

重新啟動 ComfyUI。

📝 使用說明 (Usage)

api_key: 請填入你在 MuleRouter 取得的 API Key。

mode:

Generate_New: 建立新影片生成任務。

Recover_Task: 找回並下載之前的任務（需配合 force_task_id 使用）。