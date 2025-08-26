# PDF 浮水印工具

一個基於 Streamlit 的 PDF 浮水印應用程式，提供直觀的介面來為 PDF 文件添加客製化浮水印。

## 功能特色

- 📁 **檔案上傳**: 支援 PDF 檔案上傳
- 🎨 **自訂浮水印**: 可調整文字內容、字體大小、顏色 (RGB)、透明度
- 🔄 **旋轉角度**: 自由設定浮水印旋轉角度 (0-90度)
- 📏 **間距控制**: 調整浮水印文字之間的間距
- 👀 **即時預覽**: 在處理前預覽浮水印效果
- 💾 **一鍵下載**: 處理完成後直接下載帶浮水印的 PDF

## 安裝需求

```bash
pip install streamlit PyMuPDF pillow
```

## 使用方法

1. 確保專案目錄中有 `NotoSansTC-VariableFont_wght.ttf` 字型檔案
2. 執行應用程式:
   ```bash
   streamlit run run.py
   ```
3. 在瀏覽器中開啟應用程式
4. 上傳 PDF 檔案並調整浮水印參數
5. 預覽效果後生成並下載處理後的 PDF

## 檔案結構

- `run.py` - Streamlit 主應用程式
- `script.py` - 原始批次處理腳本
- `NotoSansTC-VariableFont_wght.ttf` - 中文字型檔案 (需自行添加)

## 技術棧

- **Streamlit** - Web 應用框架
- **PyMuPDF** - PDF 處理
- **Pillow (PIL)** - 圖像處理