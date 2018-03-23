import platform
import multiprocessing as mp
from crawler import *
import pymongo
import pprint
dump_threshold = 10
processes = 8
main_proc_lock = mp.Lock()
task_counter = mp.Value('i', 0)
client = pymongo.MongoClient(
    "mongodb+srv://fxy7999148:operation@mflix-3brpa.mongodb.net/test")
db = client.metacritic
games_collection = db.games
print("Connecting to Mongodb of: ")
pprint.pprint(games_collection)


def print_list(list):
    for i in range(len(list)):
        print('%3d: %s' % (i, list[i]))


def collect_links(result):
    with main_proc_lock:
        if result is not None:
            for link in result['links']:
                game_links.append(link)
            if result['next'] is not None:
                urls.append(result['next'])
        task_counter.value -= 1


def collect_games(result):
    with main_proc_lock:
        if result is not None:
            tmp_dict_game = json.dumps(result, indent=4)
            games_collection.update(# update data to MongoDB
                {"$and":[{
                    "title": result["title"]
                },{"platform":result["platform"]}]}, result, upsert=True)
            games.append(tmp_dict_game)
        task_counter.value -= 1


def output(file, array, counter=0):
    # TODO: a version for a DB
    #for index in range(len(array)):
    #    games_collection.update(
    #        {
    #            "title": array[index]["title"]
    #        }, array[index], upsert=True)
    while len(array) > 0:
        file.write(array.pop() + ',\n')
        counter += 1
    return counter


def main():
    out = open('output.json', 'w')
    out.write('[\n')

    request_lock = mp.Lock()
    last_request = mp.Value('d', 0.0)

    pool = mp.Pool(
        processes=processes,
        initializer=init,
        initargs=(last_request, request_lock))
    print('%d processes spawned' % processes)

    dumped_counter = 0
    startup = time()
    running = True

    while running:
        for i in range(processes):
            try:
                with main_proc_lock:
                    if len(games) >= dump_threshold:
                        dumped_counter = output(out, games, dumped_counter)
                        print('current execution time: %f\n%4d games dumped' %
                              (time() - startup, dumped_counter))
                    if len(urls) > 0:
                        url = urls.pop(0)
                        pool.apply_async(
                            game_list_parse, (url, 10), callback=collect_links)
                        task_counter.value += 1
                    elif len(game_links) > 0:
                        url = game_links.pop(0)
                        pool.apply_async(
                            game_page_parse, (url, 5), callback=collect_games)
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
    print('games crawled: %d' % dumped_counter)
    print('active tasks: %d' % task_counter.value)
    print_list(urls)
    print('missed list urls:')
    print_list(urls)
    print('missed game urls:')
    print_list(game_links)


if __name__ == '__main__':
    main()
