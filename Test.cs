using iTextSharp.text;
using iTextSharp.text.pdf;
using System.Collections.Generic;
using System.IO;

public class PDFManager
{
    private Document document;
    private PdfWriter writer;
    private Font font;

    public PDFManager(string outputPath)
    {
        document = new Document();
        writer = PdfWriter.GetInstance(document, new FileStream(outputPath, FileMode.Create));
        document.Open();
        font = FontFactory.GetFont(FontFactory.HELVETICA, 12);
    }

    public void AddNews(List<News> newsList)
    {
        foreach (News news in newsList)
        {
            // Haber boyutunu kontrol ederek sığdırabildiği kadar haber ekleyin
            float remainingSpace = document.PageSize.Height - document.TopMargin - document.BottomMargin - document.Bottom;
            foreach (string paragraphText in news.Paragraphs)
            {
                Paragraph paragraph = new Paragraph(paragraphText, font);
                float paragraphHeight = paragraph.CalculateHeights();

                // Eğer paragraf mevcut sayfaya sığmazsa yeni bir sayfa ekleyin
                if (paragraphHeight > remainingSpace)
                {
                    document.NewPage();
                    remainingSpace = document.PageSize.Height - document.TopMargin - document.BottomMargin - document.Bottom;
                }

                // Paragrafı sayfaya ekleyin
                document.Add(paragraph);
                remainingSpace -= paragraphHeight;
            }
        }
    }

    public void CloseDocument()
    {
        document.Close();
        writer.Close();
    }
}

public class News
{
    public List<string> Paragraphs { get; set; }

    public News()
    {
        Paragraphs = new List<string>();
    }
}

// Kullanım örneği
PDFManager pdfManager = new PDFManager("output.pdf");

// Haberleri oluşturun
List<News> newsList = new List<News>();
News news1 = new News();
news1.Paragraphs.Add("Haber 1 Paragraf 1");
news1.Paragraphs.Add("Haber 1 Paragraf 2");
newsList.Add(news1);

News news2 = new News();
news2.Paragraphs.Add("Haber 2 Paragraf 1");
news2.Paragraphs.Add("Haber 2 Paragraf 2");
newsList.Add(news2);

// Haberleri PDF'e ekleyin
pdfManager.AddNews(newsList);

pdfManager.CloseDocument();
