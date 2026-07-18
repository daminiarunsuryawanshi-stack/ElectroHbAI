import re
import pandas as pd


class DataPreprocessor:

    def __init__(self, csv_path):
        self.csv_path = csv_path

    def clean_text(self, text):
        if pd.isna(text):
            return ""

        text = str(text).lower()
        text = re.sub(r"<.*?>", "", text)
        text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def preprocess(self):

        df = pd.read_csv(
            self.csv_path,
            low_memory=False
        )

        df.drop(
            columns=[
                "Unnamed: 26",
                "Unnamed: 27",
                "Unnamed: 28",
                "Unnamed: 29",
                "Unnamed: 30"
            ],
            inplace=True,
            errors="ignore"
        )

        df.drop_duplicates(
            subset=["name"],
            inplace=True
        )

        df["brand"] = df["brand"].fillna("Unknown")
        df["manufacturer"] = df["manufacturer"].fillna("Unknown")
        df["categories"] = df["categories"].fillna("Other")
        df["imageURLs"] = df["imageURLs"].fillna("")
        df["prices.amountMin"] = df["prices.amountMin"].fillna(0)
        df["prices.amountMax"] = df["prices.amountMax"].fillna(0)
        df["prices.currency"] = df["prices.currency"].fillna("USD")
        df["prices.availability"] = df["prices.availability"].fillna("Unknown")
        df["prices.condition"] = df["prices.condition"].fillna("Unknown")
        df["weight"] = df["weight"].fillna("Unknown")

        df["name"] = df["name"].apply(self.clean_text)
        df["brand"] = df["brand"].apply(self.clean_text)
        df["manufacturer"] = df["manufacturer"].apply(self.clean_text)
        df["categories"] = df["categories"].apply(self.clean_text)

        df["combined_features"] = (
            df["name"] + " " +
            df["brand"] + " " +
            df["manufacturer"] + " " +
            df["categories"]
        )

        df.to_csv(
            "app/ml/clean_products.csv",
            index=False
        )

        print("Dataset Cleaned Successfully")
        print("Total Products :", len(df))

        return df


if __name__ == "__main__":

    processor = DataPreprocessor(
        "app/ml/dataset/DatafinitiElectronicsProductsPricingData.csv"
    )

    processor.preprocess()