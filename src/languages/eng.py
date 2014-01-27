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
						'status':'Status',
						'uh_oh': '''
Uh oh! Looks like there was a problem. 
Copy the below error to let your developer know what went wrong.

{} 		
		''',
						'error_title':"Error",
						'execution_finished':'Execution Finished', 
						'success_message': 'Program completed Sucessfully!\nPress the OK button to exit',
						
	}
	
	with open('english.json', 'wb') as f: 
		f.write(json.dumps(english,  indent=4, sort_keys=True))