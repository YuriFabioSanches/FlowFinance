
import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Github, Linkedin, Mail, Code, Database, Globe } from 'lucide-react';

const About = () => {
  const frontendTech = [
    'React', 'TypeScript', 'Vite', 'Tailwind CSS', 'Shadcn/UI', 
    'React Router', 'TanStack Query', 'React Hook Form', 'Lucide React'
  ];

  const backendTech = [
    'FastAPI', 'Python', 'SQLAlchemy', 'PostgreSQL', 'JWT Authentication',
    'Pydantic', 'Uvicorn', 'Alembic'
  ];

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-purple-800 bg-clip-text text-transparent mb-4">
          About Flow Finance
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
          A modern, full-stack personal finance management application designed to help you track expenses, 
          manage accounts, and gain insights into your financial habits.
        </p>
      </div>

      <div className="grid gap-8 md:grid-cols-2">
        {/* Project Overview */}
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Globe className="w-5 h-5" />
              Project Overview
            </CardTitle>
            <CardDescription>
              Learn more about Flow Finance and its features
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-gray-700 dark:text-gray-300">
              Flow Finance is a comprehensive personal finance management system that enables users to:
            </p>
            <ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300 ml-4">
              <li>Track income and expenses with detailed categorization</li>
              <li>Manage multiple financial accounts</li>
              <li>Import and export transaction data</li>
              <li>Visualize financial data through interactive charts</li>
              <li>Secure user authentication and data protection</li>
              <li>Responsive design for desktop and mobile devices</li>
            </ul>
            <p className="text-gray-700 dark:text-gray-300">
              Built with modern web technologies, Flow Finance offers a seamless user experience 
              with real-time data synchronization and intuitive user interface design.
            </p>
          </CardContent>
        </Card>

        {/* Frontend Stack */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Code className="w-5 h-5" />
              Frontend Technologies
            </CardTitle>
            <CardDescription>
              Modern React-based frontend stack
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {frontendTech.map((tech) => (
                <Badge key={tech} variant="secondary" className="text-xs">
                  {tech}
                </Badge>
              ))}
            </div>
            <Separator className="my-4" />
            <div className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
              <p><strong>Framework:</strong> React 18 with TypeScript for type safety</p>
              <p><strong>Build Tool:</strong> Vite for fast development and optimized builds</p>
              <p><strong>Styling:</strong> Tailwind CSS with Shadcn/UI components</p>
              <p><strong>State Management:</strong> TanStack Query for server state</p>
              <p><strong>Routing:</strong> React Router for client-side navigation</p>
            </div>
          </CardContent>
        </Card>

        {/* Backend Stack */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Database className="w-5 h-5" />
              Backend Technologies
            </CardTitle>
            <CardDescription>
              High-performance Python API backend
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {backendTech.map((tech) => (
                <Badge key={tech} variant="outline" className="text-xs">
                  {tech}
                </Badge>
              ))}
            </div>
            <Separator className="my-4" />
            <div className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
              <p><strong>Framework:</strong> FastAPI for high-performance async API</p>
              <p><strong>Database:</strong> PostgreSQL with SQLAlchemy ORM</p>
              <p><strong>Authentication:</strong> JWT-based secure authentication</p>
              <p><strong>Validation:</strong> Pydantic for data validation and serialization</p>
              <p><strong>Migrations:</strong> Alembic for database schema management</p>
            </div>
          </CardContent>
        </Card>

        {/* Developer Section */}
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Project Developer</CardTitle>
            <CardDescription>
              Meet the person behind Flow Finance
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-start space-x-4">
              <div className="w-16 h-16 bg-gradient-to-r from-purple-600 to-purple-800 rounded-full flex items-center justify-center">
                <span className="text-white font-bold text-xl">YS</span>
              </div>
              <div className="flex-1">
                <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                  Yuri Fabio Sanches
                </h3>
                <p className="text-gray-600 dark:text-gray-400 mb-3">
                  Full-Stack Developer & Software Engineer
                </p>
                <p className="text-gray-700 dark:text-gray-300 mb-4">
                  Passionate about creating modern, user-friendly applications that solve real-world problems. 
                  Experienced in both frontend and backend development with a focus on clean code, 
                  performance optimization, and exceptional user experiences.
                </p>
                <div className="flex space-x-3">
                  <Badge variant="outline" className="flex items-center gap-1">
                    <Github className="w-3 h-3" />
                    GitHub
                  </Badge>
                  <Badge variant="outline" className="flex items-center gap-1">
                    <Linkedin className="w-3 h-3" />
                    LinkedIn
                  </Badge>
                  <Badge variant="outline" className="flex items-center gap-1">
                    <Mail className="w-3 h-3" />
                    Contact
                  </Badge>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Footer */}
      <div className="text-center py-8">
        <Separator className="mb-6" />
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Flow Finance &copy; 2024 - Built with ❤️ using modern web technologies
        </p>
      </div>
    </div>
  );
};

export default About;
