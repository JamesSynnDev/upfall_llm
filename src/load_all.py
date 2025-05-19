import pdfplumber
import fitz  # pymupdf
import pandas as pd
import os

pdf_path = '../data/document.pdf'
output_dir = '../store/pdf_extracted_content'
os.makedirs(output_dir, exist_ok=True)

content_sequence = []
table_count = 0
image_count = 0

# PyMuPDF로 이미지 추출 준비
doc = fitz.open(pdf_path)

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages):
        page_height = page.height

        # 표 추출 (pdfplumber)
        tables = page.extract_tables()
        table_objs = page.find_tables()
        table_contents = []
        for table, obj in zip(tables, table_objs):
            table_contents.append({
                'type': 'table',
                'y0': obj.bbox[1],
                'content': table
            })

        # 텍스트 추출
        text_blocks = page.extract_words(use_text_flow=True, keep_blank_chars=True)
        text_content = ' '.join([word['text'] for word in text_blocks])
        if text_blocks:
            min_y = min([word['top'] for word in text_blocks])
            text_contents = {
                'type': 'text',
                'y0': min_y,
                'content': text_content
            }
        else:
            text_contents = None

        # 이미지 추출 (PyMuPDF 사용)
        img_list = []
        fitz_page = doc.load_page(page_num)
        for img in fitz_page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image['image']
            image_ext = base_image['ext']
            image_count += 1
            img_path = os.path.join(output_dir, f'image_{page_num+1}_{image_count}.{image_ext}')
            with open(img_path, 'wb') as img_file:
                img_file.write(image_bytes)

            # 이미지 위치 정보 얻기
            img_rects = fitz_page.get_image_rects(xref)
            if img_rects:
                y0 = img_rects[0].y0
            else:
                y0 = page_height  # 기본값 설정

            img_list.append({
                'type': 'image',
                'y0': y0,
                'content': img_path
            })

        # 전체 콘텐츠 병합 후 페이지 위에서 아래로 정렬
        combined_content = table_contents + img_list
        if text_contents:
            combined_content.append(text_contents)
        combined_content.sort(key=lambda x: x['y0'])

        # 결과를 콘텐츠 시퀀스에 추가
        for item in combined_content:
            if item['type'] == 'table':
                table_count += 1
                df = pd.DataFrame(item['content'])
                table_path = os.path.join(output_dir, f'table_{page_num+1}_{table_count}.csv')
                df.to_csv(table_path, index=False, encoding='utf-8-sig')
                content_sequence.append(('table', table_path))
            elif item['type'] == 'image':
                content_sequence.append(('image', item['content']))
            else:
                content_sequence.append(('text', item['content']))

# 전체 콘텐츠 시퀀스 저장
result_df = pd.DataFrame(content_sequence, columns=['type', 'content'])
result_csv_path = os.path.join(output_dir, 'pdf_content_sequence.csv')
result_df.to_csv(result_csv_path, index=False, encoding='utf-8-sig')

print(f"추출 완료! 결과 저장 위치: {output_dir}")