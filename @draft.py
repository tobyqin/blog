from codecs import open
from datetime import date
from os.path import join, dirname, abspath

current_path = dirname(__file__)
draft_path = abspath(join(current_path, '_drafts'))
template_file = join(draft_path, 'draft-template.md')


def read_template():
    with open(template_file, encoding='utf8') as f:
        return f.read()


if __name__ == '__main__':
    print('Creating new draft post...\n')
    print('Title:')
    title = input()

    print('Category: Tech (default)')
    category = input()
    if not category:
        category = 'Tech'

    tags = ''
    while not tags:
        print('Tags: (required)')
        tags = input()

    category = ','.join(category.split())
    tags = ','.join(tags.split())

    content = read_template()
    content = content.replace('$title', title)
    content = content.replace('$category', category)
    content = content.replace('$tags', tags)
    content = content.replace('$date', date.today().isoformat())

    draft_name = title.strip().replace(' ', '-') + '.md'
    draft_name = join(draft_path, draft_name)
    with open(draft_name, encoding='utf8', mode='w') as f:
        f.write(content)

    print('\nOK, draft created.\n{}'.format(draft_name))
