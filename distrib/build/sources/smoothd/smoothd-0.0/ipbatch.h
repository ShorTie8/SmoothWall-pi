/* SmoothWall helper program - header file
 *
 * Written by Martin Houston <martin.houston@smoothwall.net>
 * This program is distributed under the terms of the GNU General Public
 * Licence.  See the file COPYING for details.
 *
 * filename: ipbatch.h
 */
 
#ifndef __IPBATCH_H
#define __IPBATCH_H
#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>
// C++ side
#include <string>
#include <cstring>
#include <iostream>
#define BATCHSTORE_SIZE 65536

// this only actualy does something if one of the args is "commit"
// in which case a non zero return code indicates some failure.
int ipbatch(const char *arg);
int ipbatch(const std::string & arg);
int ipbatch(std::vector<std::string> &arg);

// this is here because its handy to use with ipbatch.
inline std::string stringprintf(const char *fmt, ...) 
{
	va_list argp;
	char buffer[BATCHSTORE_SIZE]; // should be enough for most cases - if not malloc
	std::string retstr = "";
	va_start(argp, fmt);
	
	vsnprintf(buffer, BATCHSTORE_SIZE - 1, fmt, argp);
	retstr = buffer;

	return retstr;
}
#endif
