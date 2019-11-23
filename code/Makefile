RAPIDXML = ./include/rapidxml-1.13/
IDIR = ./include/
CC = g++
CFLAGS = -I$(IDIR) -I$(RAPIDXML) -std=c++11

ODIR = ./build
EDIR = ./bin
SDIR = ./src

_OBJ1 = doc.o
OBJ1 = $(patsubst %,$(ODIR)/%,$(_OBJ1))

_OBJ2 = query.o
OBJ2 = $(patsubst %,$(ODIR)/%,$(_OBJ2))

$(ODIR)/%.o: $(SDIR)/%.cpp
	$(CC) -c -o $@ $< $(CFLAGS)

doc: $(OBJ1)
	$(CC) -o $(EDIR)/$@ $^ $(CFLAGS)

query: $(OBJ2)
	$(CC) -o $(EDIR)/$@ $^ $(CFLAGS)

.PHONY: clean

clean:
	rm -f $(ODIR)/*.o $(EDIR)/query $(EDIR)/doc
