from wayback import WaybackClient
from wayback import Mode
import re
import io
from os import path
import pdb

def main():
    """
    Main function
    :return: None
    """

    client = WaybackClient()
    results = client.search('blogs.securiteam.com')
    find_dmitry = re.compile(r'^.*\!dmitry.*$', re.IGNORECASE)
    bad_digests = list()
    time_slice = 86400 * 365 * 5  #5 years

    for r in results:
        digest = r[5]
        if digest not in bad_digests and digest:
            try:
                response = client.get_memento(r, mode=Mode.original, exact=False, target_window=time_slice)
                content = response.content.decode()
            except Exception as e:
                print("Failed to retrieve memento for digest {}. Error {}".format(digest, e))
                content = ""
                bad_digests.append(digest)

            for line in content.split('\n'):
                found = re.search(find_dmitry, line, flags=0)
                if found:
                    ret = write_file(digest, content)
                    if not ret:
                        print("Error writing out digest {}".format(digest))




def write_file(name, content):
    """
    write html to disk
    :param name: a unique name for the file
    :param content: the contents of the file
    :return: boolean
    """
    file_name = "{}.html".format(name)
    if path.exists(file_name):
        print("File {} already exists. Returning".format(file_name))
        return True

    try:
        with io.open(file_name, "w", encoding="utf-8") as fh:
            fh.write(content)
            fh.close()
    except Exception as e:
        print("Failed to write content to {}. Error: {}".format(file_name, e))
        return False

    return True


if __name__ == "__main__":
    print("Searching Wayback....")
    main()
