#!/bin/sh

# Check and install dependencies based on the lockfile available
if [ -f yarn.lock ]; then
    echo "Installing dependencies with Yarn..."
    yarn install --frozen-lockfile
elif [ -f package-lock.json ]; then
    echo "Installing dependencies with npm..."
    npm ci
elif [ -f pnpm-lock.yaml ]; then
    echo "Installing dependencies with pnpm..."
    corepack enable pnpm
    pnpm install --frozen-lockfile
else
    echo "Error: Lockfile not found. Cannot determine package manager."
    exit 1
fi
