mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
[theme]
primaryColor='#85878a'
backgroundColor='#000000'
secondaryBackgroundColor='#212123'
textColor='#454848'
" > ~/.streamlit/config.toml
