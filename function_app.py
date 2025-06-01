import logging
import azure.functions as func
from PyPDF2 import PdfReader, PdfWriter
from azure.storage.blob import BlobServiceClient
import os
import io

app = func.FunctionApp()

# Temp for debugging
@app.function_name(name="hello")
@app.route(route="hello")
def hello_func(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("Hello from Azure Functions!")

@app.function_name(name="split_pdf_on_upload_func")
@app.blob_trigger(arg_name="myblob", path="ivana-jiahao-ben/Experiments/01_incoming-PDFs/{name}",
                  connection="geagpkilab2025_STORAGE")
def split_pdf_on_upload_func(myblob: func.InputStream):

    blob_data = myblob.read()  # Read the blob stream into memory
    pdf_file = io.BytesIO(blob_data)  # Wrap in BytesIO to make it seekable
    reader = PdfReader(pdf_file)

    # Read the PDF content
    # reader = PdfReader(myblob)
    num_pages = len(reader.pages)

    # Connect to blob service
    conn_str = os.getenv("geagpkilab2025_STORAGE")
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    output_container = "ivana-jiahao-ben"

    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)

        output_stream = io.BytesIO()
        writer.write(output_stream)
        output_stream.seek(0)

        blob_name = f"Experiments/02_split-PDF-pages/{myblob.name.removesuffix('.pdf').removeprefix('ivana-jiahao-ben/Experiments/01_incoming-PDFs/')}_page_{i+1}.pdf"
        blob_client = blob_service_client.get_blob_client(container=output_container, blob=blob_name)
        blob_client.upload_blob(output_stream, overwrite=True)

        logging.info(f"Uploaded split page: {blob_name}")
    

####################

# @app.blob_trigger(path="ivana-jiahao-ben/Experiments/incoming-PDFs/{name}",
#                   connection="AzureWebJobsStorage")
# def split_pdf_on_upload_func(myblob: func.InputStream, name: str):
#     logging.info(f"Python blob trigger function processed blob Name: {name}, Size: {myblob.length} Bytes")

#     try:
#         # Read the content of the blob into an in-memory byte stream
#         pdf_stream = io.BytesIO(myblob.read())

#         # Now pass the seekable in-memory stream to PdfReader
#         reader = PdfReader(pdf_stream)

#         # You can now proceed with your PDF splitting logic
#         # Example: Print the number of pages
#         logging.info(f"Number of pages in {name}: {len(reader.pages)}")

#         # Example: Split and save pages (conceptual)
#         for page_num in range(len(reader.pages)):
#             writer = PdfWriter()
#             writer.add_page(reader.pages[page_num])
#             output_stream = io.BytesIO()
#             writer.write(output_stream)
#             # Here you would typically upload output_stream to another blob
#             # For local testing, you might save it to a file:
#             # with open(f"output_page_{page_num}.pdf", "wb") as f:
#             #     f.write(output_stream.getvalue())

#     except Exception as e:
#         logging.error(f"Error processing PDF: {e}")