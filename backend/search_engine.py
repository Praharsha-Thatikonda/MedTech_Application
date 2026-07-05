class SearchEngine:
    @staticmethod
    def search(query, items, keys=['name', 'specialty', 'tags', 'location']):
        """
        Simple keyword search implementation.
        query: str
        items: list of dicts
        keys: fields to search in
        """
        query = query.lower()
        results = []
        
        for item in items:
            score = 0
            for k in keys:
                val = str(item.get(k, '')).lower()
                if query in val:
                    score += 1
            
            if score > 0:
                results.append(item)
                
        return results

    @staticmethod
    def filter_by_availability(items):
        return [i for i in items if i.get('status') == 'Available' or i.get('status') == 'Open']

search_engine = SearchEngine()
