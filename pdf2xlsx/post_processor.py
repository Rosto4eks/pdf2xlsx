import pandas as pd

class PostProcessor():
    def __init__(
        self,
        index_col_pos=0,
        fix_index=True,
        separate_policy = "table", # "page", "table" "none"
        has_header_on_new_page=True,
    ):
        self.index_col_pos=index_col_pos
        self.fix_index = fix_index
        self.separate_policy = separate_policy
        self.has_header_on_new_page = has_header_on_new_page

    def __isNewTable(self, index_list: pd.Series) -> bool:
        try:
            numeric_values = pd.to_numeric(index_list, errors='coerce')
            return ((numeric_values >= 1) & (numeric_values <= 10)).any()
        except:
            return False
    
    def __separate_by_page(self, dfs) -> list[pd.DataFrame]:
        return dfs
    
    def __separate_by_table(self, dfs) -> list[pd.DataFrame]:
        table = pd.DataFrame()
        tables = []
        for df in dfs:
            if self.__isNewTable(df[df.columns[0]]):
                if not table.empty:
                    tables.append(table)
                table = df
            else:
                if self.has_header_on_new_page:
                    df = df.iloc[1:]
                table = pd.concat([table, df])    
        tables.append(table)
        return tables
    
    def __separate_none(self, dfs) -> list[pd.DataFrame]:
        table = pd.DataFrame()
        for i, df in enumerate(dfs):
            if i == 0:
                table = df
            else:
                if self.has_header_on_new_page:
                    df = df.iloc[1:]
                table = pd.concat([table, df])    
        return [table]
    
    def process(self, raw_tables):
        dfs = []
        for table in raw_tables:
            df = pd.DataFrame(table)
            df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)

            if df.empty:
                continue  
            dfs.append(df)
        
        if self.separate_policy == "page":
            dfs = self.__separate_by_page(dfs)
        elif self.separate_policy == "table":
            dfs = self.__separate_by_table(dfs)
        else:
            dfs = self.__separate_none(dfs)

        return dfs
