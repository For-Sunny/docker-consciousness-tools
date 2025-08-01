#!/usr/bin/env node
/**
 * MCP Filesystem Server Diagnostic
 * Tests if the filesystem server can be run manually
 */

import { spawn } from 'child_process';
import path from 'path';

console.log('MCP Filesystem Server Diagnostic');
console.log('================================\n');

const serverPath = 'C:\\Users\\Pirate\\AppData\\Roaming\\Claude\\Claude Extensions\\ant.dir.ant.anthropic.filesystem\\server\\index.js';
const targetPath = 'C:\\Users\\Pirate\\Desktop\\DOCKER_CONSCIOUSNESS_TOOLS';

console.log(`Server Path: ${serverPath}`);
console.log(`Target Path: ${targetPath}`);
console.log('\nAttempting to start server...\n');

const server = spawn('node', [serverPath, targetPath], {
  stdio: 'inherit',
  shell: true
});

server.on('error', (err) => {
  console.error('Failed to start server:', err);
});

server.on('exit', (code) => {
  console.log(`Server exited with code ${code}`);
});

// Keep the process alive
process.stdin.resume();
