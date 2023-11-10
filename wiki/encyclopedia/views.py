from django.shortcuts import render,HttpResponse, redirect
from django.contrib import messages
from . import util
from .forms import EntryForm


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def htmlentry(request, q):
    content = util.get_entry(q)
    context = {'contents': content, 'search_query': q}

    if content is not None:
        return render(request, "encyclopedia/entry.html", context)
    else:
        return HttpResponse(f"Entry with title '{q}' not found.")

def entry(request):
    q = request.GET.get('q', '')

    if not q:
        q = "default_value_here"
    
    all_entries = util.list_entries()
    matching_entries = [entry for entry in all_entries if q.lower() in entry.lower()]

    content = util.get_entry(q)
    context = {'contents': content, 'search_query': q.capitalize, 'results': matching_entries}

    if content is not None:
        return render(request, "encyclopedia/entry.html", context)
    elif matching_entries: 
        return render(request, "encyclopedia/searchresult.html", context)
    else:
        return HttpResponse(f"Entry with title '{q}' not found.")
    
# def edit(request, title):
#     if request.method == 'POST':
#         form = form.EntryForm(request.POST)
#         if form.is_valid():
#             new_content = form.cleaned_data['content']
#             # Save the edited entry content
#             util.save_entry(new_title, new_content)

#             # Redirect to the edited entry's page
#             return redirect('entry_detail', title=new_title)
#     else:
#         form = EditEntryForm(initial={'title': title, 'content': entry_content})

#     return render(request, "encyclopedia/edit_entry.html", {'form': form, 'entry_title': title})

def create(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            checker = util.get_entry(title)
            if checker is not None:
                messages.error(request, 'Entry Already Exist, If you wish to edit an Entry kindly use the Edit button on the Entry')
            else:
                util.save_entry(title, content)
                return redirect('encyclopedia:info_path', q=title)
    else:
        form = EntryForm()
    return render(request, "encyclopedia/create.html", {'form': form})
