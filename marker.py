# Installation cell - run this FIRST
#marker is ocr tool which is used for create for bank statements 
!pip install marker-pdf
!pip install torch torchvision
!apt-get install -y poppler-utils tesseract-ocr
!pip install PyPDF2  # Fallback option

Step 02:
# Method 1: Using Marker (Recommended)
def convert_pdf_with_marker(pdf_path, output_dir="marker_out"):
    """
    Convert PDF using Marker with OCR
    """
    try:
        from marker.converters.pdf import PdfConverter
        from marker.models import create_model_dict
        from marker.output import text_from_rendered

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        print("🔄 Loading Marker models...")
        # Load models
        model_dict = create_model_dict()

        print(f"🔄 Converting PDF: {pdf_path}")
        # Create converter
        converter = PdfConverter(
            artifact_dict=model_dict,
        )

        # Convert PDF
        rendered = converter(pdf_path)

        # Extract text and metadata
        text, _, images = text_from_rendered(rendered)

        # Save output
        output_file = os.path.join(output_dir, "output.md")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"✅ Done! Output saved to: {output_file}")
        return text

    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("\n📦 Please install Marker:")
        print("!pip install marker-pdf")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def send_to_groq_llm(text, question="Summarize this document"):
    """
    Send to Groq (FREE & FAST API)
    Get free API key from: https://console.groq.com
    """
    try:
        GROQ_API_KEY = "##################################################"  # Replace karo

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-70b-versatile",  # Free model
                "messages": [
                    {"role": "user", "content": f"{question}\n\n{text}"}
                ],
                "temperature": 0.7
            }
        )

        result = response.json()
        return result['choices'][0]['message']['content']

    except Exception as e:
        print(f"❌ Groq Error: {e}")
        return None

# Main execution
if __name__ == "__main__":
    # Your PDF path
    pdf_file = "/content/Hdfcbank.pdf"
    output_directory = "/content/marker_out"

    print("=" * 60)
    print("🚀 Starting PDF Conversion with Marker")
    print("=" * 60)

    # Try Method 1
    print("\n📌 Trying Method 1 (PdfConverter)...")
    result = convert_pdf_with_marker(pdf_file, output_directory)

    if result is None:
        # Try Method 2
        print("\n📌 Trying Method 2 (Alternative API)...")
        result = convert_pdf_marker_alternative(pdf_file, output_directory)

    if result is None:
        # Try Method 3 (Your original style)
        print("\n📌 Trying Method 3 (Original Style)...")
        result, images, meta = convert_pdf_original_style(pdf_file, output_directory)

    if result is None:
        # Try fallback
        print("\n📌 Trying Method 4 (Fallback - PyPDF2)...")
        result = convert_pdf_fallback(pdf_file, os.path.join(output_directory, "output.txt"))

    if result:
        print("\n" + "=" * 60)
        print("✅ SUCCESS! PDF converted successfully")
        print("=" * 60)
        print(f"\n📄 Preview (first 500 chars):\n")
        print(result[:500] + "..." if len(result) > 500 else result)
    else:
        print("\n" + "=" * 60)
        print("❌ All methods failed. See error messages above.")
        print("=" * 60)
