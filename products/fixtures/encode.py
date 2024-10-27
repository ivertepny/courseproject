with open('products.json', 'r', encoding='windows-1251') as f:
    content = f.read()

with open('products_utf8.json', 'w', encoding='utf-8') as f:
    f.write(content)

if __name__ == '__main__':
    pass
