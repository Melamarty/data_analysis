from fpdf import FPDF




class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Netflix Data Analysis Report', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_figure(self, title, image_path):
        self.add_page()
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'C')
        self.image(image_path, x=10, y=30, w=180)
        self.ln(85)

if __name__ == "__main__":
    pdf = PDF()
    pdf.add_figure('Number of Movies by Country', 'output/movies_by_country.png')
    pdf.add_figure('TV Shows and Movies by Year Range', 'output/shows_movies_by_year_range.png')
    pdf.add_figure('Movies by Duration', 'output/movies_by_duration.png')
    pdf.add_figure('TV Shows by Season', 'output/shows_by_season.png')
    pdf.output('output/netflix_report.pdf')
