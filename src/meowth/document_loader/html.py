from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import HTMLSemanticPreservingSplitter


class HTMLDocumentManager:
    def __init__(self, directory_path, glob_pattern="./**/*.html"):
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
            loader_cls=TextLoader,
            )
        self.documents = loader.load()
        print(f"=====Loaded {len(self.documents)} documents")
        #print(f"=====First document: {self.documents[0]}")
        #print(f"=====Last document: {self.documents[-1]}")

    def split_documents(self):
        headers_to_split_on = [("h1", "Header 1"), ("h2", "Header 2"), ("h3", "Header 3"), ("h4", "Header 4")]
        text_splitter = HTMLSemanticPreservingSplitter(
            headers_to_split_on=headers_to_split_on,
            preserve_links=True,
            elements_to_preserve=["table", "ul", "ol", "code"],
            denylist_tags=["script", "style", "head"],
        )
        for doc in self.documents:
            print(f"=====Splitting document {doc.metadata['source']}")
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

            print(f"=====Split {len(sections)} sections")
            self.all_sections.extend(sections)

        print(f"=====Split {len(self.all_sections)} sections")
        #print(f"=====First section: {self.all_sections[0]}")
        #print(f"=====Last section: {self.all_sections[-1]}")
