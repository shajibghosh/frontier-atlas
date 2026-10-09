import json,unittest
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'data/atlas.json').read_text(encoding='utf-8'))
class AtlasTests(unittest.TestCase):
    def test_unique_ids_and_count(self):
        ids=[p['id'] for p in DATA['problems']]
        self.assertEqual(len(ids),100)
        self.assertEqual(len(set(ids)),100)
    def test_domain_balance(self):
        self.assertEqual(dict(Counter(p['domain'] for p in DATA['problems'])),{x:20 for x in ['Physics','Chemistry','Genetics','Psychology','Physiology']})
    def test_three_level_taxonomy(self):
        self.assertEqual(len(set((p['domain'],p['topic']) for p in DATA['problems'])),25)
        self.assertEqual(len(set((p['domain'],p['topic'],p['subtopic']) for p in DATA['problems'])),50)
    def test_citations_resolve(self):
        for p in DATA['problems']:
            self.assertTrue(p['refs'])
            for key in p['refs']:
                self.assertIn(key,DATA['sources'])
                self.assertTrue(DATA['sources'][key]['url'].startswith('https://'))
    def test_derived_static_site(self):
        self.assertEqual((ROOT/'docs/index.html').read_bytes(),(ROOT/'FrontierAtlas_Interactive.html').read_bytes())
        self.assertIn('id="atlas-data"',(ROOT/'docs/index.html').read_text(encoding='utf-8'))
if __name__=='__main__':unittest.main()
