 public float CalculateParagraphHeight(iTextSharp.text.Paragraph paragraph, PdfWriter writer, iTextSharp.text.Document document)
        {
            // PdfContentByte nesnesi oluşturun
            PdfContentByte canvas = writer.DirectContent;

            // ColumnText nesnesi oluşturun
            ColumnText column = new ColumnText(canvas);
            column.AddElement(paragraph);
            column.SetSimpleColumn(40, 0, 555, 842); // Genişlik ve yükseklik ayarlarını dilediğiniz gibi ayarlayabilirsiniz
            column.Go();
            //document.NewPage();
            // Yüksekliği hesaplayın
            float lineHeight = column.YLine;
            canvas.Reset();
            
            return document.PageSize.Height - lineHeight; 
            
        }
        public void AddNews(List<News> newsList, iTextSharp.text.Document document, PdfWriter writer)
        {
            float remainingSpace = document.PageSize.Height - document.TopMargin - document.BottomMargin - document.Bottom - (239);
            foreach (News news in newsList)
            {
                // Haber boyutunu kontrol ederek sığdırabildiği kadar haber ekle
                iTextSharp.text.Paragraph newsParagraph = new iTextSharp.text.Paragraph();
                foreach (iTextSharp.text.Paragraph paragraph in news.Paragraphs)
                {
                    newsParagraph.Add(paragraph);
                }

                float paragraphHeight = CalculateParagraphHeight(newsParagraph, writer,document);

                // Eğer paragraf mevcut sayfaya sığmazsa yeni bir sayfa ekle
                if (paragraphHeight > remainingSpace)
                {
                    document.NewPage();
                    remainingSpace = document.PageSize.Height - document.TopMargin - document.BottomMargin - document.Bottom;
                }

                //Paragrafı sayfaya ekle
                document.Add(newsParagraph);
                remainingSpace -= paragraphHeight;
            }
        }

        private void CreateDocuments(List<NewsEntity> newsEntities)
        {
            List<NewsEntity> yurtDisiHaberler = newsEntities.Where(p => p.WebSiteName != "DefenceTurk" && p.WebSiteName != "DefenceTurkey" && p.WebSiteName != "SavunmaSanayist").ToList();
            List<NewsEntity> yurtIciHaberler = newsEntities.Where(p => p.WebSiteName == "DefenceTurk" || p.WebSiteName == "DefenceTurkey" || p.WebSiteName == "SavunmaSanayist").ToList();


            string bitisDateText = newsEntities.OrderByDescending(p => p.PublishDate).ToList().FirstOrDefault().PublishDate.ToString("dd.MM.yyyy");
            string baslangicDateText = newsEntities.OrderBy(p => p.PublishDate).ToList().FirstOrDefault().PublishDate.ToString("dd.MM.yyyy");

            using (var reader = new PdfReader(@"C:\Users\s20128\Desktop\MedyaTakipDocumentFormat_v2\medyatakip.pdf"))
            {
                using (var fileStream = new FileStream(@"C:/Users/s20128/Desktop/MedyaTakipDocumentFormat_v2/MedyaTakipBelge.pdf", FileMode.Create, FileAccess.Write))
                {
                    iTextSharp.text.Document document = new iTextSharp.text.Document(iTextSharp.text.PageSize.A4, 40, 40, 0, 0);
                    var writer = PdfWriter.GetInstance(document, fileStream);

                    document.Open();

                    iTextSharp.text.Image headerImage = iTextSharp.text.Image.GetInstance("C:/Users/s20128/Desktop/MedyaTakipDocumentFormat_v2/Capture.JPG");

                    headerImage.Alignment = Element.ALIGN_TOP;
                    headerImage.ScaleToFit(600f, 200f);
                    headerImage.Alignment = iTextSharp.text.Image.TEXTWRAP | iTextSharp.text.Image.ALIGN_CENTER;
                    document.Add(headerImage);
                    iTextSharp.text.Paragraph Date = new iTextSharp.text.Paragraph(new Chunk(baslangicDateText + " - " + bitisDateText, FontFactory.GetFont(FontFactory.TIMES_BOLD, 12, iTextSharp.text.Font.NORMAL)));
                    Date.Alignment = Element.ALIGN_CENTER;
                    document.Add(Date);
                    document.Add(new Chunk("\n\n\n"));

                    for (var i = 1; i <= reader.NumberOfPages; i++)
                    {
                        var baseFont = BaseFont.CreateFont(BaseFont.HELVETICA, BaseFont.CP1252, BaseFont.NOT_EMBEDDED);
                        var titleFont = BaseFont.CreateFont(BaseFont.HELVETICA_BOLD, BaseFont.CP1252, BaseFont.NOT_EMBEDDED);
                        var importedPage = writer.GetImportedPage(reader, i);

                        PdfContentByte contentByte = writer.DirectContent;

                        PdfContentByte titleByte = writer.DirectContent;

                        string newsContent = "";
                        

                        if (yurtIciHaberler.Any())
                        {
                            iTextSharp.text.Paragraph yurtIciHaberlerTitle = new iTextSharp.text.Paragraph(new Chunk("YURT ICI KAYNAKLI HABERLER", FontFactory.GetFont(FontFactory.TIMES_BOLD, 12, iTextSharp.text.Font.NORMAL)));
                            yurtIciHaberlerTitle.Alignment = Element.ALIGN_CENTER;
                            document.Add(yurtIciHaberlerTitle);

                            List<News> newList = new List<News>();
                            for (int y = 0; y < yurtIciHaberler.Count; y++)
                            {
                                News news1 = new News();

                                var anchor = new Chunk("Devami için tiklayiniz.")
                                {
                                    Font = new iTextSharp.text.Font(iTextSharp.text.Font.FontFamily.TIMES_ROMAN, 11, iTextSharp.text.Font.NORMAL, BaseColor.BLUE)
                                };
                                string[] sentences = Regex.Split(yurtIciHaberler[y].Text, @"(?<=[\.!\?])\s+");

                                foreach (var sentence in sentences)
                                {
                                    newsContent += sentence.Replace('ş', 's').Replace('ü', 'u').Replace('ı', 'i').Replace('ö', 'o').Replace('ğ', 'g').Replace('ç', 'c').Replace('Ü', 'U')
                                        .Replace('Ş', 'S').Replace('İ', 'I').Replace('Ğ', 'G').Replace('Ö', 'O');
                                    if (newsContent.Length >= 1000)
                                    {
                                        anchor.SetAnchor(yurtIciHaberler[y].Url);
                                        break;
                                    }
                                }
                                iTextSharp.text.Paragraph paragraph = new iTextSharp.text.Paragraph(new Chunk(newsContent, FontFactory.GetFont(FontFactory.TIMES_ROMAN, 11, iTextSharp.text.Font.NORMAL)));
                                if (newsContent.Length >= 1000)
                                {
                                    paragraph.Add("\n");
                                    paragraph.Add(anchor);
                                }

                                if (yurtIciHaberler[y].Title.Contains("Haber Merkezi"))
                                {
                                    yurtIciHaberler[y].Title = yurtIciHaberler[y].Title.Substring(0, yurtIciHaberler[y].Title.IndexOf("Haber Merkezi"));
                                }
                                yurtIciHaberler[y].Title = yurtIciHaberler[y].Title.Replace('ş', 's').Replace('ü', 'u').Replace('ı', 'i').Replace('ö', 'o').Replace('ğ', 'g').Replace('ç', 'c').Replace('Ü', 'U')
                                        .Replace('Ş', 'S').Replace('İ', 'I').Replace('Ğ', 'G').Replace('Ö', 'O');
                                iTextSharp.text.Paragraph title = new iTextSharp.text.Paragraph(new Chunk(yurtIciHaberler[y].Title, FontFactory.GetFont(FontFactory.TIMES_BOLD, 16, iTextSharp.text.Font.NORMAL)));
                                iTextSharp.text.Paragraph date = new iTextSharp.text.Paragraph(new Chunk(yurtIciHaberler[y].PublishDate.ToString("dd.MM.yyyy"), FontFactory.GetFont(FontFactory.TIMES_ITALIC, 11, iTextSharp.text.Font.NORMAL)));
                                iTextSharp.text.Paragraph newsSource = new iTextSharp.text.Paragraph(new Chunk(yurtIciHaberler[y].WebSiteName, FontFactory.GetFont(FontFactory.TIMES_ROMAN, 11, iTextSharp.text.Font.NORMAL)));
                                int index = !yurtIciHaberler[y].Url.Contains(".net") ? yurtIciHaberler[y].Url.IndexOf(".com") : yurtIciHaberler[y].Url.IndexOf(".net");
                                iTextSharp.text.Paragraph newsUrl = new iTextSharp.text.Paragraph(new Chunk(yurtIciHaberler[y].Url.Substring(0, index + 4), FontFactory.GetFont(FontFactory.TIMES_ITALIC, 11, iTextSharp.text.Font.NORMAL)));
                                
                                
                                paragraph.Alignment = Element.ALIGN_JUSTIFIED;
                                title.Alignment = Element.ALIGN_CENTER;
                                date.Alignment = Element.ALIGN_RIGHT;
                                newsSource.Alignment = Element.ALIGN_RIGHT;
                                newsUrl.Alignment = Element.ALIGN_LEFT;

                                iTextSharp.text.Paragraph nl = new iTextSharp.text.Paragraph(new Chunk("\n\n\n"));
                                //document.Add();
                                news1.Paragraphs.Add(nl);
                                news1.Paragraphs.Add(title);
                                news1.Paragraphs.Add(date);
                                news1.Paragraphs.Add(newsSource);
                                //document.Add(title);
                                //document.Add(new Chunk("\n"));
                                nl = new iTextSharp.text.Paragraph(new Chunk("\n"));
                                //document.Add(date);
                               // document.Add(newsSource);
                               // document.Add(new Chunk("\n"));
                                news1.Paragraphs.Add(nl);

                                

                                if (yurtIciHaberler[y].Image != null)
                                {
                                    try
                                    {
                                        iTextSharp.text.Image img = iTextSharp.text.Image.GetInstance(yurtIciHaberler[y].Image);
                                        img.ScaleToFit(250f, 250f);
                                        img.Alignment = iTextSharp.text.Image.TEXTWRAP | iTextSharp.text.Image.ALIGN_CENTER;
                                        img.IndentationLeft = 9f;
                                        img.SpacingAfter = 9f;

                                        document.Add(img);
                                        document.Add(new Chunk("\n"));
                                    }
                                    catch
                                    {
                                        document.Add(new Chunk("\n"));
                                    }
                                }

                                news1.Paragraphs.Add(paragraph);
                                news1.Paragraphs.Add(nl);
                                news1.Paragraphs.Add(newsUrl);
                                //document.Add(paragraph);
                                //document.Add(new Chunk("\n"));
                                //document.Add(newsUrl);

                                newList.Add(news1);

                                newsContent = "";
                                //document.NewPage();
                            }
                            AddNews(newList, document, writer);
                        }
