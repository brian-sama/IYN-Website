# Testimonials - Admin Guide

## ✅ What Was Fixed

### 1. **Database Integration**
- Testimonials page now pulls data from the database
- All 6 existing testimonials have been loaded into the database
- You can now add, edit, and delete testimonials from the admin panel

### 2. **Photo Upload Support**
The photo field already existed in the model, and now it's fully functional:
- Upload photos in the admin panel
- Photos will display on the testimonials page
- If no photo is uploaded, a placeholder image is used

---

## 📋 How to Manage Testimonials

### **To Add a New Testimonial:**

1. Go to: `http://127.0.0.1:8000/admin/`
2. Navigate to: **Core** → **Testimonials**
3. Click **"Add Testimonial"**
4. Fill in the fields:
   - **Name**: Person's full name
   - **Role**: Their title/position and country (e.g., "Youth Entrepreneur, Zimbabwe")
   - **Country**: Select from dropdown
   - **Photo**: Upload a photo (optional but recommended)
   - **Content**: Their testimonial text
   - **Rating**: 1-5 stars (usually 5)
   - **✅ Is approved**: **MUST CHECK THIS** for it to appear on the website
   - **Is featured**: Check to feature on homepage
5. Click **"Save"**

### **Important:**
- ✅ New testimonials **MUST** have **"is_approved"** checked to appear on the website
- This is a security feature to prevent spam/inappropriate content
- All 6 existing testimonials are already approved

---

## 🖼️ Photo Guidelines

**Recommended specs:**
- **Size**: 400x300 pixels (or similar 4:3 ratio)
- **Format**: JPG or PNG
- **Max file size**: 10MB

**If no photo is uploaded:**
- The system uses placeholder images from Unsplash
- These are professional stock photos that rotate

---

## ✏️ How to Edit Existing Testimonials

1. Admin Panel → **Core** → **Testimonials**
2. Click on the testimonial name
3. Make your changes
4. Click **"Save"**
5. Changes appear immediately on the website

---

## 🗑️ How to Remove a Testimonial

**Option 1: Hide it (recommended)**
1. Click on the testimonial
2. **Uncheck** "is_approved"
3. Click "Save"
4. It will no longer appear on the website (but stays in database)

**Option 2: Delete permanently**
1. Select the checkbox next to the testimonial
2. Choose **"Delete selected testimonials"** from the dropdown
3. Click "Go"
4. Confirm deletion

---

## 📊 Testimonials in the Database

**Currently loaded:**
1. Tanaka Moyo - Youth Entrepreneur, Zimbabwe
2. Thabo Ndlovu - Community Leader, South Africa
3. Rumbi Chikwanha - Advocacy Coordinator, Zimbabwe
4. Sipho Mthembu - Tech Innovator, South Africa
5. Chipo Mutasa - Environmental Activist, Zimbabwe
6. Mandla Khumalo - Arts Program Director, South Africa

All are **approved** and **featured**.

---

## 🔍 Where Testimonials Appear

1. **Testimonials Page**: `/testimonials/` - All approved testimonials
2. **Homepage**: Featured testimonials (if "is_featured" is checked)

---

## 💡 Pro Tips

1. **Use real photos** when possible - they build more trust
2. **Keep testimonials concise** - 2-3 sentences is ideal
3. **Highlight different programs** - showcase variety
4. **Update regularly** - add new success stories as they come in

---

*Last updated: 2025-11-23*
