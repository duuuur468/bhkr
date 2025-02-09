import camelot
import pandas as pd

def extract_and_calculate(pdf_file: str) -> float:
    # Extract all tables from the PDF
    tables = camelot.read_pdf(pdf_file, pages="all")
    
    if not tables:
        raise ValueError("No tables found in the PDF file.")
    
    # Concatenate all tables into a single DataFrame
    df = pd.concat([table.df for table in tables], ignore_index=True)
    
    # Assuming the first row is the header with column names:
    df.columns = df.iloc[0]
    df = df[1:]
    
    # Optional: Display the columns for debugging
    # print("Columns identified:", df.columns.tolist())
    
    # Expected columns: "Group", "Maths", "English", "Physics", "Economics", "Biology"
    # Convert necessary columns to numeric values
    marks_columns = ["Maths", "English", "Physics", "Economics", "Biology"]
    for col in marks_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    
    # Convert Group column to numeric as well so that we can filter based on group number
    df["Group"] = pd.to_numeric(df["Group"], errors="coerce")
    
    # Filter: Groups between 1 and 35 (inclusive) and English marks 49 or above
    filtered_df = df[(df["Group"] >= 1) & (df["Group"] <= 35) & (df["English"] >= 49)]
    
    # Sum the Maths marks of the filtered students
    total_maths = filtered_df["Maths"].sum()
    return total_maths

if __name__ == "__main__":
    # Specify the path to the PDF file containing student marks
    pdf_file_path = "data/student_marks.pdf"  # Adjust the path if necessary
    
    try:
        total = extract_and_calculate(pdf_file_path)
        print(f"Total Maths marks for students scoring 49 or more in English in groups 1-35: {total}")
    except Exception as e:
        print(f"Error processing the PDF: {e}")