
import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { apiClient, Transaction, Account, Category } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';
import { Plus, Edit, Trash2, Download, Upload, ArrowUpDown, TrendingUp, TrendingDown } from 'lucide-react';
import DeleteConfirmDialog from '@/components/DeleteConfirmDialog';

const Transactions: React.FC = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [deleteDialog, setDeleteDialog] = useState<{ isOpen: boolean; transaction: Transaction | null }>({
    isOpen: false,
    transaction: null,
  });
  const [editingTransaction, setEditingTransaction] = useState<Transaction | null>(null);
  const [formData, setFormData] = useState({
    amount: 0,
    description: '',
    source: '',
    date: new Date().toISOString().split('T')[0],
    account_id: 0,
    category_id: 0,
    transaction_type: 'expense' as 'expense' | 'revenue',
  });
  const { toast } = useToast();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setIsLoading(true);
      const [transactionsData, accountsData, categoriesData] = await Promise.all([
        apiClient.getTransactions(),
        apiClient.getAccounts(),
        apiClient.getCategories(),
      ]);

      setTransactions(transactionsData);
      setAccounts(accountsData);
      setCategories(categoriesData);
    } catch (error) {
      console.error('Failed to load data:', error);
      toast({
        title: "Error",
        description: "Failed to load data. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      if (editingTransaction) {
        await apiClient.updateTransaction(editingTransaction.id, formData);
        toast({
          title: "Transaction updated",
          description: "Transaction has been updated successfully.",
        });
      } else {
        await apiClient.createTransaction(formData);
        toast({
          title: "Transaction created",
          description: "New transaction has been created successfully.",
        });
      }
      
      setIsDialogOpen(false);
      resetForm();
      loadData();
    } catch (error) {
      console.error('Failed to save transaction:', error);
      toast({
        title: "Error",
        description: "Failed to save transaction. Please try again.",
        variant: "destructive",
      });
    }
  };

  const handleEdit = (transaction: Transaction) => {
    setEditingTransaction(transaction);
    setFormData({
      amount: transaction.amount,
      description: transaction.description,
      source: transaction.source,
      date: transaction.date.split('T')[0],
      account_id: transaction.account_id || 0,
      category_id: transaction.category_id || 0,
      transaction_type: transaction.transaction_type,
    });
    setIsDialogOpen(true);
  };

  const handleDeleteClick = (transaction: Transaction) => {
    setDeleteDialog({ isOpen: true, transaction });
  };

  const handleDeleteConfirm = async () => {
    if (!deleteDialog.transaction) return;
    
    try {
      await apiClient.deleteTransaction(deleteDialog.transaction.id);
      toast({
        title: "Transaction deleted",
        description: "Transaction has been deleted successfully.",
      });
      setDeleteDialog({ isOpen: false, transaction: null });
      loadData();
    } catch (error) {
      console.error('Failed to delete transaction:', error);
      toast({
        title: "Error",
        description: "Failed to delete transaction. Please try again.",
        variant: "destructive",
      });
    }
  };

  const handleExport = async () => {
    try {
      const blob = await apiClient.exportTransactions();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = 'transactions.zip';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      toast({
        title: "Export successful",
        description: "Transactions ZIP file has been downloaded successfully.",
      });
    } catch (error) {
      console.error('Failed to export transactions:', error);
      toast({
        title: "Export failed",
        description: "Failed to export transactions. Please try again.",
        variant: "destructive",
      });
    }
  };

  const handleImport = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      await apiClient.importTransactions(file);
      toast({
        title: "Import successful",
        description: "Transactions have been imported successfully.",
      });
      loadData();
    } catch (error) {
      console.error('Failed to import transactions:', error);
      toast({
        title: "Import failed",
        description: "Failed to import transactions. Please check your file format.",
        variant: "destructive",
      });
    }
    
    // Reset file input
    e.target.value = '';
  };

  const resetForm = () => {
    setFormData({
      amount: 0,
      description: '',
      source: '',
      date: new Date().toISOString().split('T')[0],
      account_id: 0,
      category_id: 0,
      transaction_type: 'expense',
    });
    setEditingTransaction(null);
  };

  const getAccountName = (accountId?: number) => {
    if (!accountId) return 'No Account';
    const account = accounts.find(a => a.id === accountId);
    return account?.name || 'Unknown Account';
  };

  const getCategoryName = (categoryId?: number) => {
    if (!categoryId) return 'No Category';
    const category = categories.find(c => c.id === categoryId);
    return category?.name || 'Unknown Category';
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-48"></div>
          <div className="flex space-x-2">
            <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded w-24"></div>
            <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded w-24"></div>
            <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded w-32"></div>
          </div>
        </div>
        <Card className="animate-pulse">
          <CardContent className="p-6">
            <div className="h-64 bg-gray-200 dark:bg-gray-700 rounded"></div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-purple-800 bg-clip-text text-transparent">
            Transactions
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Track your income and expenses
          </p>
        </div>
        
        <div className="flex space-x-2">
          <Button
            variant="outline"
            onClick={handleExport}
            className="flex items-center space-x-2"
          >
            <Download className="w-4 h-4" />
            <span>Export ZIP</span>
          </Button>
          
          <label>
            <input
              type="file"
              accept=".json"
              onChange={handleImport}
              className="hidden"
            />
            <Button
              variant="outline"
              className="flex items-center space-x-2 cursor-pointer"
              asChild
            >
              <span>
                <Upload className="w-4 h-4" />
                <span>Import</span>
              </span>
            </Button>
          </label>
          
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button
                onClick={resetForm}
                className="bg-gradient-to-r from-purple-600 to-purple-800 hover:from-purple-700 hover:to-purple-900"
              >
                <Plus className="w-4 h-4 mr-2" />
                Add Transaction
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>
                  {editingTransaction ? 'Edit Transaction' : 'Create New Transaction'}
                </DialogTitle>
                <DialogDescription>
                  {editingTransaction ? 'Update your transaction details' : 'Add a new income or expense transaction'}
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="transaction_type">Transaction Type</Label>
                  <Select
                    value={formData.transaction_type}
                    onValueChange={(value: 'expense' | 'revenue') => 
                      setFormData({ ...formData, transaction_type: value })
                    }
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="revenue">Revenue</SelectItem>
                      <SelectItem value="expense">Expense</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="amount">Amount</Label>
                  <Input
                    id="amount"
                    type="number"
                    step="0.01"
                    value={formData.amount}
                    onChange={(e) => setFormData({ ...formData, amount: parseFloat(e.target.value) || 0 })}
                    placeholder="0.00"
                    required
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="description">Description</Label>
                  <Input
                    id="description"
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    placeholder="e.g., Grocery shopping, Salary"
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="source">Source</Label>
                  <Input
                    id="source"
                    value={formData.source}
                    onChange={(e) => setFormData({ ...formData, source: e.target.value })}
                    placeholder="e.g., Supermarket, Employer"
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="date">Date</Label>
                  <Input
                    id="date"
                    type="date"
                    value={formData.date}
                    onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="account_id">Account</Label>
                  <Select
                    value={formData.account_id.toString()}
                    onValueChange={(value) => setFormData({ ...formData, account_id: parseInt(value) })}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select account" />
                    </SelectTrigger>
                    <SelectContent>
                      {accounts.map((account) => (
                        <SelectItem key={account.id} value={account.id.toString()}>
                          {account.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="category_id">Category</Label>
                  <Select
                    value={formData.category_id.toString()}
                    onValueChange={(value) => setFormData({ ...formData, category_id: parseInt(value) })}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select category" />
                    </SelectTrigger>
                    <SelectContent>
                      {categories.map((category) => (
                        <SelectItem key={category.id} value={category.id.toString()}>
                          {category.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex justify-end space-x-2 pt-4">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => setIsDialogOpen(false)}
                  >
                    Cancel
                  </Button>
                  <Button type="submit">
                    {editingTransaction ? 'Update Transaction' : 'Create Transaction'}
                  </Button>
                </div>
              </form>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <ArrowUpDown className="w-5 h-5" />
            <span>All Transactions</span>
          </CardTitle>
          <CardDescription>
            {transactions.length} transactions total
          </CardDescription>
        </CardHeader>
        <CardContent>
          {transactions.length === 0 ? (
            <div className="text-center py-12">
              <ArrowUpDown className="w-16 h-16 mx-auto text-gray-400 mb-4" />
              <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
                No transactions yet
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                Start tracking your finances by adding your first transaction
              </p>
              <Button
                onClick={() => {
                  resetForm();
                  setIsDialogOpen(true);
                }}
                className="bg-gradient-to-r from-purple-600 to-purple-800 hover:from-purple-700 hover:to-purple-900"
              >
                <Plus className="w-4 h-4 mr-2" />
                Add Your First Transaction
              </Button>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Type</TableHead>
                    <TableHead>Description</TableHead>
                    <TableHead>Amount</TableHead>
                    <TableHead>Source</TableHead>
                    <TableHead>Account</TableHead>
                    <TableHead>Category</TableHead>
                    <TableHead>Date</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {transactions.map((transaction) => (
                    <TableRow key={transaction.id}>
                      <TableCell>
                        <div className="flex items-center space-x-2">
                          {transaction.transaction_type === 'revenue' ? (
                            <TrendingUp className="w-4 h-4 text-green-600" />
                          ) : (
                            <TrendingDown className="w-4 h-4 text-red-600" />
                          )}
                          <span className="capitalize">{transaction.transaction_type}</span>
                        </div>
                      </TableCell>
                      <TableCell className="font-medium">
                        {transaction.description}
                      </TableCell>
                      <TableCell>
                        <span className={
                          transaction.transaction_type === 'revenue' 
                            ? 'text-green-600 font-medium' 
                            : 'text-red-600 font-medium'
                        }>
                          {transaction.transaction_type === 'revenue' ? '+' : '-'}
                          ${transaction.amount.toFixed(2)}
                        </span>
                      </TableCell>
                      <TableCell>{transaction.source}</TableCell>
                      <TableCell>{getAccountName(transaction.account_id)}</TableCell>
                      <TableCell>
                        <div className="flex items-center space-x-2">
                          <div className="w-3 h-3 rounded-full bg-purple-500"></div>
                          <span>{getCategoryName(transaction.category_id)}</span>
                        </div>
                      </TableCell>
                      <TableCell>
                        {new Date(transaction.date).toLocaleDateString()}
                      </TableCell>
                      <TableCell>
                        <div className="flex space-x-2">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleEdit(transaction)}
                          >
                            <Edit className="w-4 h-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleDeleteClick(transaction)}
                            className="text-red-600 hover:text-red-700"
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>

      <DeleteConfirmDialog
        isOpen={deleteDialog.isOpen}
        onOpenChange={(open) => setDeleteDialog({ isOpen: open, transaction: null })}
        onConfirm={handleDeleteConfirm}
        title="Delete Transaction"
        description="Are you sure you want to delete this transaction? This action cannot be undone."
        itemName={deleteDialog.transaction?.description}
      />
    </div>
  );
};

export default Transactions;
