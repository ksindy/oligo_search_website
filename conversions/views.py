from django.shortcuts import render
#from django import forms
from .forms import user_sequence_input, pattern_input, mismatch_input
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
    text = text.upper().replace(" ","")
    pattern = pattern.upper().replace(" ","")
    pattern_matches = ''
    pattern_location = ''
    pattern_end = 0
    pattern_found = False
    add_base = False
    if pattern == '':
        return ('')
    else:
        for i, base in enumerate(text):
            pattern_matches += '<i></i>'
            query_pattern = text[i:i+len(pattern)]
            add_base = False

            if mismatch(pattern, query_pattern) <= max_mismatches and not pattern_found:
                pattern_matches += '<b>'
                pattern_found = True
                pattern_end = i + (len(pattern)-1)
                pattern_location += str(i+1)+','+'\t'

            elif mismatch(pattern, query_pattern) <= max_mismatches and pattern_found:
                pattern_end = i + (len(pattern)-1)
                pattern_location += str(i+1)+','+'\t'

            if i == pattern_end and pattern_found:
                pattern_matches += base
                pattern_matches +='</b>'
                pattern_end = 0
                add_base = True
                pattern_found = False

            if not add_base:
                pattern_matches += base

        return(pattern_location, pattern_matches )


def test(request):
    if request.method == "POST":
        form1 = user_sequence_input(request.POST)
        form2 = pattern_input(request.POST)
        form3 = mismatch_input(request.POST)
        if form1.is_valid():
            sequence_list = []
            sequence_wrap = ''
            if (request.POST.get('Reverse Complement')):
                sequence = (form1.cleaned_data['sequence'])
                result = reverse_complement(sequence)
                result = str(result)
                sequence_list.append(result)
                print(type(sequence_list[0]))
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

            if sequence_list:
                for i, nucleotide in enumerate(sequence_list[0]):
                    sequence_wrap += nucleotide
                    sequence_wrap += '<i></i>'

        if form2.is_valid():
            mismatch_choice = int(request.POST['mismatches'])
            text = (form1.cleaned_data['sequence'])
            pattern = (form2.cleaned_data['pattern'])
            bold = approximate_patterns(text, pattern, mismatch_choice)
            #bold = "<b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A"
            #<b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T
            #print(bold)
            #print(pattern)

        return render(request, 'conversions/conversions_input.html', {'output': sequence_wrap, 'form1': form1, 'form2': form2, 'output2': bold, 'form3':form3,})
    else:
        form1 = user_sequence_input()
        form2 = pattern_input()
        form3 = mismatch_input()
    return render (request, 'conversions/conversions_input.html', {'form1': form1, 'form2':form2, 'form3':form3})



