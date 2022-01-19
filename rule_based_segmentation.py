def rbs(customer):
    """
    Segments the customers from the persona dataset and prints the features of the entered customer.

    Parameters
    ----------
    customer : str
        It should be entered as "USA_ANDROID_FEMALE_21_40"

    Returns
    -------
    None
    """
    import pandas as pd
    df = pd.read_csv("persona.csv")

    print(f"Row and Column Information of the Dataset : {df.shape}")
    print(f"Type of Variables in the Dataset : \n{df.dtypes}")
    print(f"Missing Data Number of Variables in Dataset : \n{df.isnull().sum()}")
    print(f"Quantile Values of Numeric Variables in the Dataset  : \n{df.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T}")

    agg_df = df.pivot_table(values="PRICE", index=["COUNTRY", "SOURCE", "SEX", "AGE"], aggfunc="mean").sort_values(
        by="PRICE", ascending=False)
    agg_df = agg_df.reset_index()

    agg_df["AGE_CAT"] = pd.cut(x=agg_df["AGE"], bins=[0, 20, 40, 60, 80, 100],
                               labels=["0_20", "21_40", "41_60", "61_80", "81_100"])

    agg_df["customers_level_based"] = [val[0].upper() + "_" + val[1].upper() + "_" + val[2].upper() + "_" + val[5] for
                                       val in agg_df.values]

    persona_df = agg_df.loc[:, ["customers_level_based", "PRICE"]].groupby("customers_level_based").agg("mean"). \
        sort_values(by="PRICE", ascending=False).reset_index()

    persona_df["SEGMENT"] = pd.qcut(persona_df["PRICE"], 4, labels=["D", "C", "B", "A"])
    new_user = persona_df[persona_df["customers_level_based"] == customer]

    print(f"\n\n\nSegment : {new_user.SEGMENT.values[0]}\n"
          f"Expected Income : {new_user.PRICE.values[0]}\n")


if __name__ == "__main__":
    rbs("USA_ANDROID_FEMALE_21_40")




