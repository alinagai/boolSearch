from functions import get_tokens_list, stopwords, lemma
import wikipediaapi
wiki_wiki = wikipediaapi.Wikipedia('ru')

def load_wiki():
    category = "Категория:Электроника"
    index_file = 'files/index.txt'
    wiki_page = wiki_wiki.page(category)
    doc_list = {}
    i = 1
    for p in wiki_page.categorymembers.values():
        if p.namespace == wikipediaapi.Namespace.MAIN:
            f_name= f'{i}.txt'
            with open(f'files/{f_name}', 'w') as f:
                f.write(p.text)
            doc_list[i] = p.canonicalurl
            i += 1
    with open(index_file, 'w') as file:
        file.write(f'{doc_list}\n')
    print(i)
    return i, doc_list

def token_lemma(text):
    tokens = text.split()
    tokens = stopwords(tokens)
    terms_ = lemma(tokens)
    return [term for term in terms_ if term]

def setting_list(query_token, index_):
    return [set(index_.get(token, '')) for token in query_token]

def make_invert_index(tokens_list, f_count):
    doc_ids = {}  #лист с id документов
    count_of_docs_list = {}  #лист с кол-вом вхождений слов
    for i in range(1, f_count):
        tokens = tokens_list[i]
        for word in tokens:
            if word == '':
                continue
            if word not in doc_ids:
                doc_ids[word] = set()
                count_of_docs_list[word] = 1
            else:
                count_of_docs_list[word] += 1
            doc_ids[word].add(i)
    #сортировка:
    count_sort = sorted(count_of_docs_list.items(), key=lambda d: d[1], reverse=True) #сортируем сначала по кол-ву вхождения
    words_sort = sorted(count_sort, key=lambda x: x[0])  # сортируем слова по aлфавиту
    invert_ind = {}
    with open('files/invert_indexes.txt', 'w') as f:
        for word in words_sort:
            f.write("%s\t%d\t" % (word[0], word[1]))
            id_sort = sorted(doc_ids[word[0]])  # сортировка списка номеров документа, в которое входит  слово
            invert_ind[word[0]] = []
            for i in range(len(id_sort)):
                f.write(f'{id_sort[i]}')
                invert_ind[word[0]] += [id_sort[i]]  # добавляем в словарь номер документа
                if i != len(id_sort) - 1:  #если документы еще не закончились, то разделяем их индексы
                    f.write(" ")
            f.write('\n')
        f.close()
    return invert_ind


def bool_searching(query,invert_index_, doc_list_, search_type='AND'):
    documents = []
    query_token = token_lemma(query) #токенизиуем и лемматизируем слова запроса

    tokens_to_search = setting_list(query_token, invert_index_) #образуем множество из слов запроса
    if search_type == 'AND':
        documents = [doc_list_[doc_id] for doc_id in set.intersection(*tokens_to_search)]
    if search_type == 'OR':
        documents = [doc_list_[doc_id] for doc_id in set.union(*tokens_to_search)]
    if search_type == 'NOT':
        documents = [doc_list_[doc_id] for doc_id in set.difference(*tokens_to_search)]
    return documents

def bool_searching_start():
    f_count, doc_list = load_wiki() # 1 загружаем документы
    tokens_list = get_tokens_list(f_count) # 2 токенизация и лемматизация
    invert_index = make_invert_index(tokens_list, f_count) # 3 создание инвертированного индекса
    poisk = str(input("Поиск: ")).encode('utf-8').strip().decode()
    with open('files/otvet.txt', 'w') as otv_file:
        find_urls = bool_searching(poisk, invert_index, doc_list) # 3 сам поиск
        for url in find_urls:
            otv_file.write(f'{url}\n')

bool_searching_start()