
def Insert(wxChoice, index, string, data=None):
	
	# Okay first thing is that we insert above index
	
	string_previous = string
	data_previous = data
	
	for i in range(index, wxChoice.GetCount()):
		string_current = wxChoice.GetString(i)
		data_current = wxChoice.GetClientData(i)
		
		wxChoice.SetString(i, string_previous)
		wxChoice.SetClientData(i, data_previous)
		
		string_previous = string_current
		data_previous = data_current
		
	# Append the last one
	wxChoice.Append(string_previous, data_previous)
