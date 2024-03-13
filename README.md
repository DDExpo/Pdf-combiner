# Pdf-combiner
 Extracting pdfs from archive(zip, rar) and combine them

## Why?
 So, at my job, we receive consignments as PDFs. We use a Telegram bot to combine them into 16 PDFs on one page, and it takes about 7 to 15 minutes every day to combine 80 to 110 PDFs, and up to 20 on Mondays as the number of consignments grows to around 200. One day, I decided to solve this issue.

 Now, with my solution, we can combine 600 PDFs in just one minute (on my machine!), and it can handle various page sizes from A0 to A8, as well as any number of elements per page. Want 10 PDFs on every page? No problem! Want 15, 25, 50, or even 100? Still, no problem!
## Usage
 For example we have this pdf 
![alt text](https://github.com/[DDExpo]/[Pdf-combiner]/[main]/media/example_pdf?raw=true)

## Instalation

py -3.11 -m venv venv

pip install -r requirements.txt

run main.py
