class RecursiveTextSplitter:
    def __init__(self, chunk_size=1000, chunk_overlap=200, separators=None):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", " ", ""]

    def split_text(self, text):
        splits = self._recursive_split(text, self.separators)

        return self._merge_splits(splits)

    def _recursive_split(self, text, separators):
        separator = separators[0]
        if separator:
            parts = text.split(separator)
        else:
            parts = list(text) 

        final_chunks = []
        current_chunk = ""
        for part in parts:
            if current_chunk:
                next_chunk = current_chunk + separator + part
            else:
                next_chunk = part

            if len(next_chunk) > self.chunk_size:
                if len(current_chunk) > 0:
                    final_chunks.append(current_chunk)
                    current_chunk = part
                else:
                    if len(separators) > 1:
                        final_chunks += self._recursive_split(part, separators[1:])
                    else:
                        final_chunks.append(part)
                    current_chunk = ""
            else:
                current_chunk = next_chunk

        if current_chunk:
            final_chunks.append(current_chunk)

        return final_chunks

    def _merge_splits(self, splits):
        chunks = []
        current_chunk = ""
        for split in splits:
            if len(current_chunk) + len(split) + 1 <= self.chunk_size:
                current_chunk += " " + split if current_chunk else split
            else:
                chunks.append(current_chunk)
                overlap = current_chunk[-self.chunk_overlap:] if self.chunk_overlap > 0 else ""
                current_chunk = overlap + split

        if current_chunk:
            chunks.append(current_chunk)
        return chunks
