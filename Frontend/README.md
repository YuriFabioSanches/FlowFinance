# FlowFinance Frontend

## Overview

FlowFinance is a modern financial management application built with React and TypeScript. This frontend application provides an intuitive user interface for managing personal finances, tracking expenses, and visualizing financial data.

## Tech Stack

- **Framework**: React with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **UI Components**: shadcn-ui
- **Package Manager**: npm/bun

## Getting Started

### Prerequisites

- Node.js (LTS version recommended)
- npm or bun package manager

### Installation

1. Clone the repository:
```sh
git clone <repository-url>
cd FlowFinance/Frontend
```

2. Install dependencies:
```sh
npm install
# or if using bun
bun install
```

3. Start the development server:
```sh
npm run dev
# or if using bun
bun dev
```

The application will be available at `http://localhost:5173` by default.

## Project Structure

```
Frontend/
├── src/              # Source files
├── public/           # Static assets
├── components/       # React components
├── pages/           # Page components
├── styles/          # Global styles
└── utils/           # Utility functions
```

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

### Code Style

This project uses ESLint and Prettier for code formatting. The configuration can be found in:
- `eslint.config.js`
- `.prettierrc`