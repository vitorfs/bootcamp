import re
import subprocess
from subprocess import TimeoutExpired
from bs4 import BeautifulSoup, Comment
from urllib.parse import urljoin

class Metadata:
    url = ""
    type = "" # https://ogp.me/#types
    title = ""
    description = ""
    image = ""

    def __str__(self):
        return "{url: " + self.url + ", type: " + self.type + ", title: " + self.title + ", description: " + self.description + ", image: " + self.image + "}"

class Metadatareader:

    @staticmethod
    def get_metadata_from_url_in_text(text):
        # look for the first url in the text
        # and extract the url metadata
        urls_in_text = Metadatareader.get_urls_from_text(text)
        if len(urls_in_text) > 0:
            return Metadatareader.get_url_metadata(urls_in_text[0])
        return Metadata()

    @staticmethod
    def get_urls_from_text(text):
        # look for all urls in text
        # and convert it to an array of urls
        regex = r"(?i)\b((?:https?:(?:\/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b\/?(?!@)))"
        return re.findall(regex, text)

    @staticmethod
    def get_url_metadata(url):
        # get final url after all redirections
        # then get html of the final url
        # fill the meta data with the info available
        url = Metadatareader.get_final_url(url)
        url_content = Metadatareader.get_url_content(url)
        soup = BeautifulSoup(url_content, "html.parser")
        metadata = Metadata()

        metadata.url = url
        metadata.type = "website"

        for meta in soup.findAll("meta"):
            # priorize using Open Graph Protocol
            # https://ogp.me/
            metadata.type = Metadatareader.get_meta_property(meta, "og:type", metadata.type)
            metadata.title = Metadatareader.get_meta_property(meta, "og:title", metadata.title)
            metadata.description = Metadatareader.get_meta_property(meta, "og:description", metadata.description)
            metadata.image = Metadatareader.get_meta_property(meta, "og:image", metadata.image)
            if metadata.image:
                metadata.image = urljoin(url, metadata.image)
            
        if not metadata.title and soup.title:
            # use page title
            metadata.title = soup.title.text

        if not metadata.image:
            # use first img element
            images = soup.find_all("img")
            if len(images) > 0:
                metadata.image = urljoin(url, images[0].get("src"))

        if not metadata.description and soup.body:
            # use text from body
            for text in soup.body.find_all(string=True):
                if text.parent.name != "script" and text.parent.name != "style" and not isinstance(text, Comment):
                    metadata.description += text

        if metadata.description:
            # remove white spaces and break lines
            metadata.description = re.sub("\n|\r|\t", " ", metadata.description)
            metadata.description = re.sub(" +", " ", metadata.description)
            metadata.description = metadata.description.strip()
            
        return metadata

    @staticmethod
    def get_final_url(url, timeout=5):
        # get final url after all redirections
        # get http response header
        # look for the "Location: " header
        proc = subprocess.Popen([
                    "curl",
                    "-Ls",#follow redirect 301 and silently
                    "-I",#don't download html body
                    url
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            out, err = proc.communicate(timeout=timeout)
        except TimeoutExpired:
            proc.kill()
            out, err = proc.communicate()
        header = str(out).split("\\r\\n")
        for line in header:
            if line.startswith("Location: "):
                return line.replace("Location: ", "")
        return url

    @staticmethod
    def get_url_content(url, timeout=5):
        # get url html
        proc = subprocess.Popen([
                    "curl",
                    "-i",
                    "-k",#ignore ssl certificate requisite
                    "-L",#follow redirect 301
                    url
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            out, err = proc.communicate(timeout=timeout)
        except TimeoutExpired:
            proc.kill()
            out, err = proc.communicate()
        return out

    @staticmethod
    def get_meta_property(meta, property_name, default_value=""):
        if "property" in meta.attrs and meta.attrs["property"] == property_name:
            return meta.attrs["content"]
        return default_value