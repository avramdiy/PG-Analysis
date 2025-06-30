from flask import Flask, render_template_string, Response
import pandas as pd
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

@app.route('/')
def load_dataframe():
    # Specify the path to your file
    file_path = r"C:\Users\avram\OneDrive\Desktop\TRG Week 30\pg.us.txt"

    try:
        # Load the file into a Pandas DataFrame
        df = pd.read_csv(file_path, sep=",", engine="python", parse_dates=['Date'], infer_datetime_format=True)

        # Filter rows by date range
        start_date = "1970-01-01"
        end_date = "1979-12-31"
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

        # Drop the "OpenInt" column if it exists
        if 'OpenInt' in df.columns:
            df = df.drop(columns=['OpenInt'])

        # Convert the DataFrame to an HTML table
        html_table = df.to_html(classes='table table-striped', index=False)

        # Render the HTML table in a simple template
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Procter & Gamble Data (1970-1979)</title>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        </head>
        <body>
            <div class="container">
                <h1 class="mt-5">Procter & Gamble (PG) Data (1970-1979)</h1>
                {html_table}
            </div>
        </body>
        </html>
        """
        return render_template_string(html_template)
    except Exception as e:
        return f"An error occurred while processing the file: {e}"
    
@app.route('/yearly_avg_open')
def yearly_avg_open():
    file_path = r"C:\Users\avram\OneDrive\Desktop\TRG Week 30\pg.us.txt"
    try:
        # Load and filter the DataFrame
        df = pd.read_csv(file_path, sep=",", engine="python", parse_dates=['Date'], infer_datetime_format=True)
        df = df[(df['Date'] >= "1970-01-01") & (df['Date'] <= "1979-12-31")]
        if 'OpenInt' in df.columns:
            df = df.drop(columns=['OpenInt'])

        # Calculate yearly average "Open" price
        df['Year'] = df['Date'].dt.year
        yearly_avg = df.groupby('Year')['Open'].mean()

        # Plot the data
        plt.figure(figsize=(10, 6))
        yearly_avg.plot(kind='line', marker='o', color='blue')
        plt.title('Yearly Average Open Price (1970-1979)', fontsize=16)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Average Open Price', fontsize=12)
        plt.grid(True)

        # Save the plot to a BytesIO buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return Response(buf, mimetype='image/png')
    except Exception as e:
        return f"An error occurred while processing the file: {e}"

if __name__ == '__main__':
    app.run(debug=True)
