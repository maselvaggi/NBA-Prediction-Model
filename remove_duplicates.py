#%%
def remove_duplicates(data):
    """
    This function removes the duplicate rows that may be present after adding new rows to the
    existing dataframe.  
    """
    names = data['Name'].unique()
    fix_names = []
    for i in names:
        guy = data[data['Name'] == i]    
        if len(guy['Name']) != len(guy['Date'].unique()):
            fix_names.append(i)

    #remove duplicate row for single date. Lower interger index value is correct (more recent)
    duplicates = []
    for i in fix_names:
        guy = data[data['Name'] == i]
        duplicates.append(guy.index[guy.duplicated(['Date'])].tolist())

    for i in duplicates:
        data = data.drop(index = i[0])    
    return data

#%%
if __name__ == "__main__":
    remove_duplicates()