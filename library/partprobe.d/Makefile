selfp := $(abspath $(lastword $(MAKEFILE_LIST)))
selfd := $(notdir $(patsubst %/,%,$(dir $(selfp))))

self  := $(basename $(selfd))

../$(self): module.py Makefile documentation.yml examples.yml; awk -f include.awk $< > $@

doc  := $(self)
list := -l

doc list:; ansible-doc -M .. $($@) | cat
