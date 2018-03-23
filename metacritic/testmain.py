from lxml import html
from time import time, sleep
import requests
import signal
import json
import re
import platform
import multiprocessing as mp
from crawler import *

def main():
    out = open('output.json', 'w')
	out.write('[\n')

	request_lock = mp.Lock()
	last_request = mp.Value('d', 0.0)

	pool = mp.Pool(processes = processes, initializer = init, initargs = (last_request, request_lock))
	print('%d processes spawned' %processes)

	dumped_counter = 0
	startup = time()
	running = True

	while running:
		for i in range(processes):
			try:
				with main_proc_lock:
					if len(games) >= dump_threshold:
						dumped_counter = output(out, games, dumped_counter)
						print('current execution time: %f\n%4d games dumped' %(time() - startup, dumped_counter))
					if len(urls) > 0:
						url = urls.pop(0)
						pool.apply_async(game_list_parse, (url, 10), callback = collect_links)
						task_counter.value += 1
					elif len(game_links) > 0:
						url = game_links.pop(0)
						pool.apply_async(game_page_parse, (url, 5), callback = collect_games)
						task_counter.value += 1
					elif task_counter.value == 0:
						print('Done.')
						running = False
						break

			except KeyboardInterrupt:
				print('keyboard interrupt catched\nexiting...')
				running = False
				break

	dumped_counter = output(out, games, dumped_counter)
	out.write('\n]')
	print('games crawled: %d' %dumped_counter)
	print('active tasks: %d' %task_counter.value)
	print_list(urls)
	print('missed list urls:')
	print_list(urls)
	print('missed game urls:')
	print_list(game_links)

if __name__ == '__main__':
	main()