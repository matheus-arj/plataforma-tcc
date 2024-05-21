/* eslint-disable @typescript-eslint/no-var-requires */
// import { Client } from 'pg';
// import dbconfig from '../../dbconfig.js';

const { Client } = require('pg');
const fs = require('fs');
const path = require('path');
const dbconfig = require('../../dbconfig.js');

async function runMigrations() {
  const client = new Client(dbconfig);

  try {
    await client.connect();
    console.log('Connected to Postgres database.');

    const migrationDir = path.join(__dirname, '../migrations');
    const migrationFiles = fs
      .readdirSync(migrationDir)
      .filter((file) => file.endsWith('.sql'));

    for (const file of migrationFiles) {
      const filePath = path.join(migrationDir, file);
      const sql = fs.readFileSync(filePath, 'utf8');

      console.log(`Running migration: ${file}`);

      await client.query(sql);
    }

    console.log('Migrations executed successfully.');
  } catch (error) {
    console.error('Error executing migration:', error);
  } finally {
    await client.end();
    console.log('Disconnected from Postgres database.');
  }
}

runMigrations();
