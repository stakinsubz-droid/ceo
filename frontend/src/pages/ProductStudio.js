import React, { useState } from 'react';
import { Palette, FileText, Video, Music, Code, Image, Layers, Sparkles, Download, Eye } from 'lucide-react';

const ProductStudio = () => {
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [productConfig, setProductConfig] = useState({
    type: 'ebook',
    niche: '',
    title: '',
    description: '',
    price: 29.99
  });
  const [generationStep, setGenerationStep] = useState(0);

  const productTypes = [
    {
      id: 'ebook',
      name: 'eBook',
      icon: <FileText size={32} />,
      color: '#a855f7',
      description: 'AI-generated comprehensive eBooks with professional formatting',
      avgTime: '15-20 min',
      avgPrice: '$29.99'
    },
    {
      id: 'course',
      name: 'Online Course',
      icon: <Video size={32} />,
      color: '#06b6d4',
      description: 'Full course with lessons, quizzes, and downloadable resources',
      avgTime: '30-45 min',
      avgPrice: '$97.00'
    },
    {
      id: 'template',
      name: 'Template Pack',
      icon: <Layers size={32} />,
      color: '#10b981',
      description: 'Professional templates for various use cases',
      avgTime: '10-15 min',
      avgPrice: '$19.99'
    },
    {
      id: 'graphics',
      name: 'Graphics Bundle',
      icon: <Image size={32} />,
      color: '#ec4899',
      description: 'High-quality graphics, illustrations, and design assets',
      avgTime: '20-25 min',
      avgPrice: '$39.99'
    },
    {
      id: 'music',
      name: 'Audio Pack',
      icon: <Music size={32} />,
      color: '#fbbf24',
      description: 'Royalty-free music tracks and sound effects',
      avgTime: '25-30 min',
      avgPrice: '$49.99'
    },
    {
      id: 'code',
      name: 'Code Package',
      icon: <Code size={32} />,
      color: '#ef4444',
      description: 'Ready-to-use code snippets, plugins, and tools',
      avgTime: '20-30 min',
      avgPrice: '$59.99'
    }
  ];

  const generationSteps = [
    { name: 'Research', icon: '🔍', status: generationStep >= 1 ? 'complete' : 'pending' },
    { name: 'Outline', icon: '📋', status: generationStep >= 2 ? 'complete' : 'pending' },
    { name: 'Generate', icon: '✨', status: generationStep >= 3 ? 'complete' : 'pending' },
    { name: 'Design', icon: '🎨', status: generationStep >= 4 ? 'complete' : 'pending' },
    { name: 'Polish', icon: '💎', status: generationStep >= 5 ? 'complete' : 'pending' }
  ];

  const startGeneration = () => {
    // Simulate generation progress
    let step = 0;
    const interval = setInterval(() => {
      step++;
      setGenerationStep(step);
      if (step >= 5) clearInterval(interval);
    }, 2000);
  };

  return (
    <div style={{ padding: 'var(--spacing-2xl)' }}>
      {/* Header */}
      <div style={{ marginBottom: 'var(--spacing-2xl)' }}>
        <h1 style={{
          fontSize: 'var(--font-size-4xl)',
          fontWeight: '900',
          background: 'var(--gradient-holographic)',
          backgroundSize: '200% 200%',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          animation: 'holographicShift 4s ease infinite',
          marginBottom: 'var(--spacing-sm)'
        }}>
          <Palette size={36} style={{ display: 'inline-block', marginRight: '1rem', color: '#a855f7' }} />
          PRODUCT STUDIO
        </h1>
        <p style={{ color: 'var(--color-text-secondary)', fontSize: 'var(--font-size-lg)' }}>
          Create professional digital products with AI-powered automation
        </p>
      </div>

      {/* Product Type Selection */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
        gap: 'var(--spacing-lg)',
        marginBottom: 'var(--spacing-2xl)'
      }}>
        {productTypes.map((product) => (
          <div
            key={product.id}
            onClick={() => setSelectedProduct(product)}
            className="glass"
            style={{
              padding: 'var(--spacing-xl)',
              borderRadius: 'var(--radius-xl)',
              cursor: 'pointer',
              transition: 'all var(--transition-normal)',
              border: selectedProduct?.id === product.id 
                ? `2px solid ${product.color}` 
                : '1px solid var(--color-glass-border)',
              boxShadow: selectedProduct?.id === product.id ? `0 0 20px ${product.color}40` : 'none'
            }}
          >
            <div style={{
              width: '64px',
              height: '64px',
              borderRadius: 'var(--radius-lg)',
              background: `${product.color}20`,
              border: `1px solid ${product.color}40`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: product.color,
              marginBottom: 'var(--spacing-lg)',
              boxShadow: `0 0 20px ${product.color}40`
            }}>
              {product.icon}
            </div>
            
            <h3 style={{
              fontSize: 'var(--font-size-xl)',
              fontWeight: '700',
              color: 'var(--color-text-primary)',
              marginBottom: 'var(--spacing-sm)'
            }}>
              {product.name}
            </h3>
            
            <p style={{
              fontSize: 'var(--font-size-sm)',
              color: 'var(--color-text-secondary)',
              marginBottom: 'var(--spacing-lg)',
              lineHeight: '1.6'
            }}>
              {product.description}
            </p>

            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              fontSize: 'var(--font-size-sm)'
            }}>
              <div>
                <div style={{ color: 'var(--color-text-tertiary)', fontSize: 'var(--font-size-xs)', marginBottom: '0.25rem' }}>
                  Avg. Time
                </div>
                <div style={{ color: product.color, fontWeight: '700' }}>
                  {product.avgTime}
                </div>
              </div>
              <div>
                <div style={{ color: 'var(--color-text-tertiary)', fontSize: 'var(--font-size-xs)', marginBottom: '0.25rem' }}>
                  Avg. Price
                </div>
                <div style={{ color: product.color, fontWeight: '700' }}>
                  {product.avgPrice}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Product Configuration */}
      {selectedProduct && (
        <div className="glass" style={{
          borderRadius: 'var(--radius-xl)',
          padding: 'var(--spacing-2xl)',
          border: `1px solid ${selectedProduct.color}40`,
          boxShadow: `0 0 20px ${selectedProduct.color}20`
        }}>
          <h2 style={{
            fontSize: 'var(--font-size-2xl)',
            fontWeight: '800',
            color: 'var(--color-text-primary)',
            marginBottom: 'var(--spacing-xl)',
            display: 'flex',
            alignItems: 'center',
            gap: 'var(--spacing-md)'
          }}>
            <Sparkles size={28} style={{ color: selectedProduct.color }} />
            Create {selectedProduct.name}
          </h2>

          <div style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: 'var(--spacing-lg)',
            marginBottom: 'var(--spacing-2xl)'
          }}>
            <div>
              <label style={{
                display: 'block',
                fontSize: 'var(--font-size-sm)',
                color: 'var(--color-text-secondary)',
                marginBottom: 'var(--spacing-sm)',
                textTransform: 'uppercase',
                letterSpacing: '1px'
              }}>
                Niche / Topic
              </label>
              <input
                type="text"
                value={productConfig.niche}
                onChange={(e) => setProductConfig({...productConfig, niche: e.target.value})}
                placeholder="e.g., Productivity, Fitness, Investing..."
                style={{
                  width: '100%',
                  padding: 'var(--spacing-md)',
                  background: 'rgba(15, 23, 42, 0.6)',
                  border: '1px solid rgba(6, 182, 212, 0.3)',
                  borderRadius: 'var(--radius-md)',
                  color: 'var(--color-text-primary)',
                  fontSize: 'var(--font-size-sm)',
                  outline: 'none'
                }}
              />
            </div>

            <div>
              <label style={{
                display: 'block',
                fontSize: 'var(--font-size-sm)',
                color: 'var(--color-text-secondary)',
                marginBottom: 'var(--spacing-sm)',
                textTransform: 'uppercase',
                letterSpacing: '1px'
              }}>
                Target Price
              </label>
              <input
                type="number"
                value={productConfig.price}
                onChange={(e) => setProductConfig({...productConfig, price: e.target.value})}
                style={{
                  width: '100%',
                  padding: 'var(--spacing-md)',
                  background: 'rgba(15, 23, 42, 0.6)',
                  border: '1px solid rgba(6, 182, 212, 0.3)',
                  borderRadius: 'var(--radius-md)',
                  color: 'var(--color-text-primary)',
                  fontSize: 'var(--font-size-sm)',
                  outline: 'none'
                }}
              />
            </div>

            <div style={{ gridColumn: '1 / -1' }}>
              <label style={{
                display: 'block',
                fontSize: 'var(--font-size-sm)',
                color: 'var(--color-text-secondary)',
                marginBottom: 'var(--spacing-sm)',
                textTransform: 'uppercase',
                letterSpacing: '1px'
              }}>
                Product Title
              </label>
              <input
                type="text"
                value={productConfig.title}
                onChange={(e) => setProductConfig({...productConfig, title: e.target.value})}
                placeholder="AI will suggest or you can customize..."
                style={{
                  width: '100%',
                  padding: 'var(--spacing-md)',
                  background: 'rgba(15, 23, 42, 0.6)',
                  border: '1px solid rgba(6, 182, 212, 0.3)',
                  borderRadius: 'var(--radius-md)',
                  color: 'var(--color-text-primary)',
                  fontSize: 'var(--font-size-sm)',
                  outline: 'none'
                }}
              />
            </div>

            <div style={{ gridColumn: '1 / -1' }}>
              <label style={{
                display: 'block',
                fontSize: 'var(--font-size-sm)',
                color: 'var(--color-text-secondary)',
                marginBottom: 'var(--spacing-sm)',
                textTransform: 'uppercase',
                letterSpacing: '1px'
              }}>
                Description (Optional)
              </label>
              <textarea
                value={productConfig.description}
                onChange={(e) => setProductConfig({...productConfig, description: e.target.value})}
                placeholder="AI will generate a compelling description..."
                rows={4}
                style={{
                  width: '100%',
                  padding: 'var(--spacing-md)',
                  background: 'rgba(15, 23, 42, 0.6)',
                  border: '1px solid rgba(6, 182, 212, 0.3)',
                  borderRadius: 'var(--radius-md)',
                  color: 'var(--color-text-primary)',
                  fontSize: 'var(--font-size-sm)',
                  outline: 'none',
                  resize: 'vertical'
                }}
              />
            </div>
          </div>

          {/* Generation Progress */}
          {generationStep > 0 && (
            <div style={{
              marginBottom: 'var(--spacing-2xl)',
              padding: 'var(--spacing-xl)',
              background: 'rgba(6, 182, 212, 0.05)',
              borderRadius: 'var(--radius-lg)',
              border: '1px solid rgba(6, 182, 212, 0.2)'
            }}>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                marginBottom: 'var(--spacing-lg)'
              }}>
                {generationSteps.map((step, idx) => (
                  <div key={idx} style={{ flex: 1, textAlign: 'center', position: 'relative' }}>
                    <div style={{
                      width: '48px',
                      height: '48px',
                      margin: '0 auto var(--spacing-sm)',
                      borderRadius: '50%',
                      background: step.status === 'complete' 
                        ? 'linear-gradient(135deg, #06b6d4, #10b981)'
                        : 'rgba(15, 23, 42, 0.6)',
                      border: step.status === 'complete'
                        ? '2px solid #10b981'
                        : '2px solid rgba(6, 182, 212, 0.3)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: '1.5rem',
                      boxShadow: step.status === 'complete' ? '0 0 20px rgba(16, 185, 129, 0.4)' : 'none'
                    }}>
                      {step.icon}
                    </div>
                    <div style={{
                      fontSize: 'var(--font-size-xs)',
                      fontWeight: '700',
                      color: step.status === 'complete' ? '#10b981' : 'var(--color-text-tertiary)',
                      textTransform: 'uppercase',
                      letterSpacing: '1px'
                    }}>
                      {step.name}
                    </div>
                    {idx < generationSteps.length - 1 && (
                      <div style={{
                        position: 'absolute',
                        top: '24px',
                        left: 'calc(50% + 24px)',
                        right: 'calc(-50% + 24px)',
                        height: '2px',
                        background: step.status === 'complete' && generationSteps[idx + 1].status === 'complete'
                          ? '#10b981'
                          : 'rgba(6, 182, 212, 0.2)'
                      }}></div>
                    )}
                  </div>
                ))}
              </div>
              
              {generationStep < 5 && (
                <div style={{ textAlign: 'center', color: 'var(--color-electric-cyan)' }}>
                  🤖 AI Agents are working... Step {generationStep} of 5
                </div>
              )}
              
              {generationStep === 5 && (
                <div style={{
                  textAlign: 'center',
                  padding: 'var(--spacing-lg)',
                  background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(6, 182, 212, 0.1))',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid rgba(16, 185, 129, 0.3)'
                }}>
                  <div style={{
                    fontSize: 'var(--font-size-2xl)',
                    fontWeight: '800',
                    color: '#10b981',
                    marginBottom: 'var(--spacing-sm)'
                  }}>
                    ✅ Product Generated Successfully!
                  </div>
                  <div style={{ display: 'flex', gap: 'var(--spacing-md)', justifyContent: 'center', marginTop: 'var(--spacing-lg)' }}>
                    <button className="btn-primary">
                      <Eye size={18} />
                      Preview
                    </button>
                    <button className="btn-primary">
                      <Download size={18} />
                      Download
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Action Button */}
          <button
            onClick={startGeneration}
            disabled={!productConfig.niche || generationStep > 0}
            className="btn-primary"
            style={{
              width: '100%',
              padding: 'var(--spacing-lg)',
              fontSize: 'var(--font-size-lg)',
              justifyContent: 'center'
            }}
          >
            <Sparkles size={24} />
            Generate {selectedProduct.name}
          </button>
        </div>
      )}
    </div>
  );
};

export default ProductStudio;
