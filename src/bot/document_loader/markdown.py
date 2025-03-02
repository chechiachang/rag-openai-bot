from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader


class MarkdownDocumentManager:
    def __init__(self, directory_path, glob_pattern="./**/*.md"):
        self.directory_path = directory_path
        self.glob_pattern = glob_pattern
        self.documents = []
        self.all_sections = []

    def load_documents(self):
        loader = DirectoryLoader(
            self.directory_path,
            glob=self.glob_pattern,
            show_progress=True,
            recursive=True,
            loader_cls=UnstructuredMarkdownLoader,
            loader_kwargs={"mode":"single"},
            #loader_kwargs={"mode":"elements"},
            )
        self.documents = loader.load()
        #print(f"=====Loaded {len(self.documents)} documents")
        #print(f"=====First document: {self.documents[0]}")

    def split_documents(self):
        headers_to_split_on = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3"), ("####", "Header 4")]
        text_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on,
            strip_headers=False # keep headers in the text
        )
        for doc in self.documents:
            sections = text_splitter.split_text(doc.page_content)

            for i in range(len(sections)):
                # keep metadata from the original document
                metadata = dict(doc.metadata)
                metadata.update(sections[i].metadata)
                metadata.update({"split": f"{i+1}/{len(sections)}"})
                sections[i].metadata = metadata
            #for section in sections:
            #    # keep metadata from the original document
            #    metadata = dict(doc.metadata)
            #    metadata.update(section.metadata)
            #    section.metadata = metadata

            self.all_sections.extend(sections)

        print(f"=====Split {len(self.all_sections)} sections")
        print(f"=====First section: {self.all_sections[0]}")
        print(f"=====Last section: {self.all_sections[-1]}")
