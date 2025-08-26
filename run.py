import streamlit as st
import fitz  # PyMuPDF
import os
from PIL import Image, ImageDraw, ImageFont
import io
import base64


def create_watermark_image(text, font_path, font_size, color, opacity, angle,
                          spacing, width, height):
    """建立浮水印圖片"""
    img = Image.new("RGBA", (int(width), int(height)), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    font = ImageFont.truetype(font_path, font_size)
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    rgba_color = color + (int(255 * opacity),)
    
    for y in range(0, int(height), text_height + spacing):
        for x in range(0, int(width), text_width + spacing):
            draw.text((x, y), text, font=font, fill=rgba_color)
    
    if angle != 0:
        img = img.rotate(angle, expand=1)
        
        rotated_width, rotated_height = img.size
        left = (rotated_width - width) // 2
        top = (rotated_height - height) // 2
        right = left + width
        bottom = top + height
        
        left = max(0, left)
        top = max(0, top)
        right = min(rotated_width, right)
        bottom = min(rotated_height, bottom)
        
        img = img.crop((left, top, right, bottom))
        
        if img.size != (int(width), int(height)):
            img = img.resize((int(width), int(height)), Image.Resampling.LANCZOS)
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return img_byte_arr


def add_watermark_to_pdf(pdf_file, watermark_params):
    """為 PDF 加入浮水印"""
    doc = fitz.open(stream=pdf_file, filetype="pdf")
    num_pages = doc.page_count
    
    page = doc.load_page(0)
    width, height = page.mediabox_size
    
    watermark_image = create_watermark_image(
        watermark_params['text'], 
        watermark_params['font_path'], 
        watermark_params['font_size'], 
        watermark_params['color'], 
        watermark_params['opacity'], 
        watermark_params['angle'],
        watermark_params['spacing'], 
        width, 
        height
    )
    
    for page_num in range(num_pages):
        page = doc.load_page(page_num)
        rect = page.mediabox
        page.insert_image(rect, stream=watermark_image, overlay=True)
        watermark_image.seek(0)
    
    output_buffer = io.BytesIO()
    doc.save(output_buffer)
    doc.close()
    output_buffer.seek(0)
    
    return output_buffer


def get_download_link(buffer, filename):
    """產生下載連結"""
    b64 = base64.b64encode(buffer.getvalue()).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">點擊下載處理後的 PDF</a>'
    return href


def main():
    st.set_page_config(page_title="PDF 浮水印工具", page_icon="📄", layout="wide")
    
    st.title("PDF 浮水印工具")
    st.write("上傳 PDF 檔案並加入客製化浮水印")
    
    with st.sidebar:
        st.header("浮水印設定")
        
        text = st.text_input(
            "浮水印文字", 
            value="Aiworks Confidential - 僅供 [公司名稱假設名字十二個字] 內部使用"
        )
        
        font_size = st.slider("字體大小", min_value=10, max_value=50, value=25)
        
        opacity = st.slider("透明度", min_value=0.1, max_value=1.0, value=0.3, step=0.1)
        
        angle = st.slider("旋轉角度", min_value=0, max_value=90, value=30)
        
        spacing = st.slider("文字間距", min_value=50, max_value=200, value=100)
        
        st.write("文字顏色 (RGB)")
        col1, col2, col3 = st.columns(3)
        with col1:
            r = st.number_input("R", min_value=0, max_value=255, value=128, step=1)
        with col2:
            g = st.number_input("G", min_value=0, max_value=255, value=128, step=1)
        with col3:
            b = st.number_input("B", min_value=0, max_value=255, value=128, step=1)
        
        color = (r, g, b)
        st.color_picker("顏色預覽", value=f"#{r:02x}{g:02x}{b:02x}", disabled=True)
    
    uploaded_file = st.file_uploader("選擇 PDF 檔案", type="pdf")
    
    if uploaded_file is not None:
        st.success(f"已上傳檔案: {uploaded_file.name}")
        
        if st.button("預覽浮水印效果"):
            try:
                font_path = "NotoSansTC-VariableFont_wght.ttf"
                if not os.path.exists(font_path):
                    st.error(f"字型檔案未找到: {font_path}")
                    st.info("請確保字型檔案存在於專案根目錄")
                    return
                
                doc = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
                page = doc.load_page(0)
                width, height = page.mediabox_size
                
                watermark_params = {
                    'text': text,
                    'font_path': font_path,
                    'font_size': font_size,
                    'color': color,
                    'opacity': opacity,
                    'angle': angle,
                    'spacing': spacing
                }
                
                watermark_image = create_watermark_image(
                    text, font_path, font_size, color, opacity, angle,
                    spacing, width, height
                )
                
                st.subheader("浮水印預覽")
                st.image(watermark_image, caption="浮水印效果", use_column_width=True)
                
                doc.close()
                
            except Exception as e:
                st.error(f"預覽時發生錯誤: {str(e)}")
        
        if st.button("生成帶浮水印的 PDF"):
            try:
                font_path = "NotoSansTC-VariableFont_wght.ttf"
                if not os.path.exists(font_path):
                    st.error(f"字型檔案未找到: {font_path}")
                    st.info("請確保字型檔案存在於專案根目錄")
                    return
                
                watermark_params = {
                    'text': text,
                    'font_path': font_path,
                    'font_size': font_size,
                    'color': color,
                    'opacity': opacity,
                    'angle': angle,
                    'spacing': spacing
                }
                
                with st.spinner("正在處理 PDF..."):
                    output_buffer = add_watermark_to_pdf(uploaded_file.getvalue(), watermark_params)
                
                st.success("PDF 處理完成!")
                
                download_filename = f"watermarked_{uploaded_file.name}"
                st.markdown(
                    get_download_link(output_buffer, download_filename), 
                    unsafe_allow_html=True
                )
                
            except Exception as e:
                st.error(f"處理 PDF 時發生錯誤: {str(e)}")
    
    else:
        st.info("請先上傳 PDF 檔案")
    
    with st.expander("使用說明"):
        st.write("""
        1. 在左側邊欄調整浮水印參數
        2. 上傳要加入浮水印的 PDF 檔案
        3. 點擊「預覽浮水印效果」查看浮水印樣式
        4. 點擊「生成帶浮水印的 PDF」處理檔案
        5. 下載處理後的 PDF 檔案
        
        **注意事項:**
        - 需要 NotoSansTC-VariableFont_wght.ttf 字型檔案
        - 支援中文字體顯示
        - 浮水印會套用到所有頁面
        """)


if __name__ == "__main__":
    main()