import streamlit as st
import pandas as pd

st.set_page_config(page_title='Vacayzen | Driver Sign-offs', page_icon='📸', layout="centered", initial_sidebar_state="auto", menu_items=None)


st.caption('VACAYZEN')
st.title('Driver Sign-offs')
st.info('View driver notes and pictures for dispatch activities.')
st.success('Data updated each day at: **6:30 - 7:00 AM**, **12:00 - 12:30 PM**, and **4:30 - 5:00 PM** CST.')

l, r = st.columns([1,2])

df = pd.read_csv(st.secrets['driveURL'] + st.secrets['fileID'], index_col=False)
df = df.rename(columns={'ID': 'Order'})
search_option = l.selectbox('Search on:', ['Order','Name','Location'])
option = r.selectbox(f'**Vacayzen** {search_option}', options=df[search_option].unique())
df = df[df[search_option] == option]

st.divider()

if df.shape[0] > 0:

    df['Sign-off'] = pd.to_datetime(df['Sign-off'])
    df['Order Start'] = pd.to_datetime(df['Order Start'])
    df['Order End'] = pd.to_datetime(df['Order End'])

    def remove_asterisks_from_driver_notes(row):
        return row.Note.replace('*','')
    
    df.Note = df.apply(remove_asterisks_from_driver_notes, axis=1)


    st.subheader(df.Name.iloc[0])
    st.caption(f'ORDER {df.Order.iloc[0]}')
    st.caption(df.Location.iloc[0])
    st.write(df['Order Start'].iloc[0])
    st.write(df['Order End'].iloc[0])
    st.divider()

    position = 0
    l, m, r = st.columns(3)

    def show_picture_details(row):
        global position
        height = 105
        match position:
            case 0:
                l.write(f'**{row.Activity}**')
                l.write(row['Sign-off'])
                if not pd.isna(row['Note']):
                    with l.container(height=height, border=False):
                        st.write(row['Note'])
                l.image(st.secrets['imageURL']+row['Image'])
                position = 1
            case 1:
                m.write(f'**{row.Activity}**')
                m.write(row['Sign-off'])
                if not pd.isna(row['Note']):
                    with m.container(height=height, border=False):
                        st.write(row['Note'])
                m.image(st.secrets['imageURL']+row['Image'])
                position = 2
            case 2:
                r.write(f'**{row.Activity}**')
                r.write(row['Sign-off'])
                if not pd.isna(row['Note']):
                    with r.container(height=height, border=False):
                        st.write(row['Note'])
                r.image(st.secrets['imageURL']+row['Image'])
                position = 0
    
    df.apply(show_picture_details, axis=1)

else:

    st.warning(f'Data for **{option}** is not available.')
