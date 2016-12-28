INCLUDE=include/
CFLAGS=-I$(INCLUDE) -std=c99
OBJS := bin/main.o bin/computation.o bin/linkedlist.o bin/queue.o bin/squeue.o bin/wsqueue.o bin/thread_pool.o

all: main

# link
main: $(OBJS)
	gcc -pthread $(OBJS) -o main

# pull in dependency info for *existing* .o files
-include $(OBJS:.o=.d)

# compile and generate dependency info;
# more complicated dependency computation, so all prereqs listed
# will also become command-less, prereq-less targets
#   sed:    strip the target (everything before colon)
#   sed:    remove any continuation backslashes
#   fmt -1: list words one per line
#   sed:    strip leading spaces
#   sed:    add trailing colons
bin/%.o: src/%.c
	mkdir -p bin
	gcc -c $(CFLAGS) src/$*.c -o bin/$*.o
	gcc -MM $(CFLAGS) src/$*.c > bin/$*.d
	@mv -f bin/$*.d bin/$*.d.tmp
	@sed -e 's|.*:|$*.o:|' < bin/$*.d.tmp > bin/$*.d
	@sed -e 's/.*://' -e 's/\\$$//' < bin/$*.d.tmp | fmt -1 | \
	  sed -e 's/^ *//' -e 's/$$/:/' >> bin/$*.d
	@rm -f bin/$*.d.tmp

# remove compilation products
clean:
	rm -rf main bin/*.o bin/*.d *.d bin/
