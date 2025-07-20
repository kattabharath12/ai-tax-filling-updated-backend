# Tax Engine - Auto-filling Tax System

A comprehensive tax filing system with automatic document processing, form filling, and payment integration.

## 🚀 Features

- **Document Processing**: Upload and automatically extract data from tax documents (W-2, 1099, receipts)
- **Smart Form Filling**: AI-powered tax form completion with validation
- **Tax Calculator**: Real-time tax calculations with current tax brackets
- **Payment Integration**: Secure tax payment and refund processing
- **Multi-user Support**: Role-based access control for individuals and tax professionals
- **Real-time Calculations**: Dynamic tax calculations with current tax rules
- **Audit Trail**: Complete logging and tracking of all tax-related activities

## 🏗️ Architecture

### Backend (FastAPI)
- **Authentication Module**: JWT-based authentication with role management
- **Document Module**: File upload, OCR processing, and data extraction
- **Forms Module**: Tax form management and auto-filling
- **Tax Engine**: Core tax calculation and validation logic
- **Payments Module**: Payment processing and transaction management
- **Admin Module**: Administrative functions and reporting

### Frontend (React)
- **Dashboard**: Overview of tax filing status and quick actions
- **Document Upload**: Drag-and-drop interface for document management
- **Form Editor**: Interactive tax form completion
- **Tax Calculator**: Real-time tax calculation tool
- **Payment Portal**: Secure payment processing interface
- **Profile Management**: User settings and preferences

### Database (MySQL)
- Users and authentication
- Document storage and metadata
- Tax forms and calculations
- Payment transactions
- Audit logs and notifications

## 🛠️ Tech Stack

- **Backend**: FastAPI, SQLAlchemy, MySQL, Redis, Celery
- **Frontend**: React, Material-UI, React Query, Axios
- **Infrastructure**: Docker, Docker Compose
- **AI/ML**: Tesseract OCR, scikit-learn for tax calculations
- **Security**: JWT tokens, bcrypt password hashing, HTTPS

## 📦 Installation

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Node.js 18+

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd tax-engine
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the application**
   ```bash
   make up
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Development Setup

1. **Install dependencies**
   ```bash
   make install
   ```

2. **Start development servers**
   ```bash
   make dev
   ```

## 🗄️ Database Schema

The system uses MySQL with the following main tables:
- `users` - User accounts and profiles
- `documents` - Uploaded tax documents
- `tax_forms` - Tax form data and status
- `payments` - Payment transactions
- `audit_logs` - System activity tracking

## 🔧 Configuration

Key configuration options in `.env`:

```env
# Database
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/tax_engine

# Security
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Upload
MAX_FILE_SIZE=50000000
UPLOAD_DIR=uploads

# External APIs
IRS_API_KEY=your-irs-api-key
PAYMENT_GATEWAY_KEY=your-payment-gateway-key
```

## 🧪 Testing

Run the test suite:
```bash
make test
```

## 📊 API Documentation

The API documentation is automatically generated and available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control
- File upload validation
- SQL injection prevention
- HTTPS enforcement in production

## 🚀 Deployment

### Production Deployment

1. **Set production environment variables**
2. **Build and deploy with Docker**
   ```bash
   docker-compose up --build -d
   ```

### Environment Variables for Production
- Set `ENVIRONMENT=production`
- Use strong `SECRET_KEY`
- Configure proper database credentials
- Set up SSL certificates
- Configure email SMTP settings

## 📝 Usage

### For Individual Users
1. Register an account
2. Upload tax documents (W-2, 1099, receipts)
3. Use the tax calculator to estimate liability
4. Review auto-filled tax forms
5. Submit and pay taxes

### For Tax Professionals
1. Create professional account
2. Manage multiple client accounts
3. Bulk document processing
4. Generate reports and analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the API docs at `/docs`

## 🔄 Changelog

### v1.0.0
- Initial release
- Core tax filing functionality
- Document processing with OCR
- Tax calculation engine
- Payment integration
- Multi-user support
- React frontend with Material-UI
- FastAPI backend with SQLAlchemy
- Docker containerization