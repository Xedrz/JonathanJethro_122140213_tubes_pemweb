import requests
from datetime import datetime

class OpenLibraryService:
    BASE_URL = "https://openlibrary.org"
    
    @classmethod
    def search_books(cls, query):
        """Mencari buku di OpenLibrary"""
        url = f"{cls.BASE_URL}/search.json"
        params = {'q': query}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            books = []
            for doc in data.get('docs', [])[:10]:  # Batasi hasil
                book = {
                    'openlibrary_id': doc.get('key', '').split('/')[-1],
                    'title': doc.get('title', 'No title'),
                    'author': ', '.join(doc.get('author_name', ['Unknown'])),
                    'published_date': cls._parse_published_date(doc.get('first_publish_year')),
                    'cover_url': cls._get_cover_url(doc.get('cover_i')),
                    'description': doc.get('first_sentence', [''])[0] if isinstance(doc.get('first_sentence'), list) else None,
                    'pages': doc.get('number_of_pages_median')
                }
                books.append(book)
                
            return books
        except Exception as e:
            print(f"Error searching books: {e}")
            return []
    
    @classmethod
    def get_book_details(cls, openlibrary_id):
        """Mendapatkan detail buku dari OpenLibrary"""
        url = f"{cls.BASE_URL}/works/{openlibrary_id}.json"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            book = {
                'openlibrary_id': openlibrary_id,
                'title': data.get('title', 'No title'),
                'author': ', '.join(data.get('author_name', ['Unknown'])),
                'published_date': cls._parse_published_date(data.get('first_publish_year')),
                'cover_url': cls._get_cover_url(data.get('covers', [None])[0] if isinstance(data.get('covers'), list) else None),
                'description': data.get('description', {}).get('value') if isinstance(data.get('description'), dict) else data.get('description'),
                'pages': data.get('number_of_pages')
            }
            
            return book
        except Exception as e:
            print(f"Error getting book details: {e}")
            return None
    
    @staticmethod
    def _parse_published_date(year):
        if year:
            try:
                return datetime(year, 1, 1).date()
            except:
                return None
        return None
    
    @staticmethod
    def _get_cover_url(cover_id):
        if cover_id:
            return f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
        return None