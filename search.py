import json
import os
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SemanticSearch:
    """Semantic search over Kuczynski's philosophical positions"""
    
    def __init__(self, database_path, embeddings_path=None):
        print(f"Loading database from {database_path}...")
        with open(database_path, 'r', encoding='utf-8') as f:
            db = json.load(f)
        
        self.positions = []
        seen_ids = set()
        
        # Handle new array-based format (v19 complete and v25)
        if 'positions' in db and isinstance(db['positions'], list):
            for pos_data in db['positions']:
                # Handle both 'id' (v25) and 'position_id' (v19) formats
                pos_id = pos_data.get('id', '') or pos_data.get('position_id', '')
                if pos_id and pos_id not in seen_ids:
                    # Handle multiple text field names across versions
                    position_text = (pos_data.get('text_evidence', '') or 
                                   pos_data.get('description', '') or
                                   pos_data.get('thesis', '') or 
                                   pos_data.get('position', '') or 
                                   pos_data.get('content', ''))
                    self.positions.append({
                        'position_id': pos_id,
                        'text': position_text,
                        'domain': pos_data.get('domain', 'Unknown'),
                        'title': pos_data.get('title', ''),
                        'source': pos_data.get('source', []) if isinstance(pos_data.get('source'), list) else [pos_data.get('source', 'Unknown')]
                    })
                    seen_ids.add(pos_id)
        
        # Handle old nested dictionary format (v17/v18)
        elif 'integrated_core_positions' in db:
            # Load from integrated_core_positions
            for domain, pos_dict in db['integrated_core_positions'].items():
                for pos_id, pos_data in pos_dict.items():
                    if pos_id not in seen_ids:
                        position_text = pos_data.get('position', '') or pos_data.get('thesis', '')
                        self.positions.append({
                            'position_id': pos_id,
                            'text': position_text,
                            'domain': domain,
                            'title': pos_data.get('title', ''),
                            'source': pos_data.get('source', []) if isinstance(pos_data.get('source'), list) else [pos_data.get('source', 'Unknown')]
                        })
                        seen_ids.add(pos_id)
            
            # Load from positions_detailed (v19 additions and other detailed positions)
            if 'positions_detailed' in db:
                for domain, pos_dict in db['positions_detailed'].items():
                    if isinstance(pos_dict, dict):
                        for pos_id, pos_data in pos_dict.items():
                            if pos_id not in seen_ids:
                                # Extract text from 'content' or 'thesis' field
                                position_text = pos_data.get('content', '') or pos_data.get('thesis', '')
                                # Get context if available for richer representation
                                if 'context' in pos_data and pos_data['context']:
                                    position_text = position_text + " " + pos_data['context']
                                
                                self.positions.append({
                                    'position_id': pos_id,
                                    'text': position_text,
                                    'domain': domain,
                                    'title': pos_data.get('title', ''),
                                    'source': [pos_data.get('work_id', 'Unknown')]
                                })
                                seen_ids.add(pos_id)
        
        print(f"Loaded {len(self.positions)} philosophical positions")
        
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        if embeddings_path and os.path.exists(embeddings_path):
            print(f"Loading pre-computed embeddings from {embeddings_path}...")
            with open(embeddings_path, 'rb') as f:
                self.embeddings = pickle.load(f)
            
            # Validate embeddings match database
            if self.embeddings.shape[0] != len(self.positions):
                print(f"⚠️  WARNING: Embeddings ({self.embeddings.shape[0]}) don't match database ({len(self.positions)})")
                print("Regenerating embeddings...")
                self.embeddings = self.model.encode([p['text'] for p in self.positions], show_progress_bar=True)
                if embeddings_path:
                    print(f"Saving new embeddings to {embeddings_path}...")
                    with open(embeddings_path, 'wb') as f:
                        pickle.dump(self.embeddings, f)
        else:
            print("Computing embeddings (this may take a minute)...")
            self.embeddings = self.model.encode([p['text'] for p in self.positions], show_progress_bar=True)
            if embeddings_path:
                print(f"Saving embeddings to {embeddings_path}...")
                os.makedirs(os.path.dirname(embeddings_path), exist_ok=True)
                with open(embeddings_path, 'wb') as f:
                    pickle.dump(self.embeddings, f)
        
        print("Semantic search initialized successfully!")
    
    def search(self, query, top_k=5, min_similarity=0.25):
        """
        Find most relevant positions for query
        
        Args:
            query: User's question or statement
            top_k: Number of results to return
            min_similarity: Minimum similarity threshold (0-1). Default 0.25 filters out weak matches.
            
        Returns:
            list of dicts with position_id, text, title, domain, similarity_score
        """
        query_embedding = self.model.encode([query])[0]
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        
        # Filter by minimum similarity threshold
        valid_indices = [i for i, sim in enumerate(similarities) if sim >= min_similarity]
        
        if not valid_indices:
            # No positions meet threshold - return empty list
            print(f"Warning: No positions found with similarity >= {min_similarity}")
            return []
        
        # Get top_k from valid indices
        valid_similarities = similarities[valid_indices]
        top_relative_indices = valid_similarities.argsort()[-min(top_k, len(valid_indices)):][::-1]
        top_indices = [valid_indices[i] for i in top_relative_indices]
        
        results = []
        for idx in top_indices:
            results.append({
                **self.positions[idx],
                'similarity': float(similarities[idx])
            })
        
        return results
