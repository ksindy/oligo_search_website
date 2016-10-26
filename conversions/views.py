from django.shortcuts import render
#from django import forms
from .forms import user_sequence_input, pattern_input
import re

def reverse_complement(text):
    text = text[::-1]
    reverse_complement_text = text.translate(str.maketrans('ACGTacgt','TGCAtgca'))
    return reverse_complement_text

def mismatch (string1, string2):
    mismatches = 0
    for (nucleotide1, nucleotide2) in zip(string1, string2):
        if nucleotide1 != nucleotide2:
            mismatches += 1
    return(mismatches)

def approximate_patterns(text, pattern, max_mismatches):
    pattern_matches = []
    for i in range(len(text)-len(pattern)+1):
        query_pattern = text[i:i+len(pattern)]
        if mismatch(pattern, query_pattern) <= max_mismatches:
            pattern_matches.append(i)
    return(pattern_matches)

def test(request):
    if request.method == "POST":
        form1 = user_sequence_input(request.POST)
        form2 = pattern_input(request.POST)
        if form1.is_valid():
            sequence_list = []
            if (request.POST.get('Reverse Complement')):
                sequence = (form1.cleaned_data['sequence'])
                result = reverse_complement(sequence)
                sequence_list.append(result)
            if (request.POST.get('Upper Case')):
                if sequence_list:
                    result = sequence_list[0].upper()
                    sequence_list[0] = result
                else:
                    result = (form1.cleaned_data['sequence']).upper()
                    sequence_list.append(result)
            if (request.POST.get('Lower Case')):
                if sequence_list:
                    result = sequence_list[0].lower()
                    sequence_list[0] = result
                else:
                    result = (form1.cleaned_data['sequence']).lower()
                    sequence_list.append(result)
            if (request.POST.get('Remove Spaces')):
                if sequence_list:
                    result = sequence_list[0].replace(" ","")
                    sequence_list[0] = result
                else:
                    result = (form1.cleaned_data['sequence']).replace(" ","")
                    sequence_list.append(result)
        if form2.is_valid():
            text = (form1.cleaned_data['sequence'])
            pattern = (form2.cleaned_data['pattern'])
            pattern_found = approximate_patterns(text,pattern ,0)
            bold = pattern_found
        return render(request, 'conversions/conversions_input.html', {'output': sequence_list, 'form1': form1, 'form2': form2, 'output2': bold})
    else:
        form1 = user_sequence_input()
        form2 = pattern_input()
    return render (request, 'conversions/conversions_input.html', {'form1': form1, 'form2':form2})



