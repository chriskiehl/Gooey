'''
Created on Jan 25, 2014

@author: Chris
'''

import json 


if __name__ == '__main__':
	english = {
						'settings':'Settings', 
						'cancel':'Cancel',
						'next':'Next',
						'simple_config':'Enter Command Line Arguments',
						'required_args_msg':'Required Arguments', 
						'optional_args_msg':'Optional Arguments',
						'running':'Running',
						"sure_you_want_to_exit":"Are you sure you want to exit?",
						'close_program': 'Close Program?',
						'status':'Status'
	}
	
	with open('english.json', 'wb') as f: 
		f.write(json.dumps(english,  indent=4, sort_keys=True))