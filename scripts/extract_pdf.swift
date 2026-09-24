import Foundation
import PDFKit
import CoreGraphics
import ImageIO

guard CommandLine.arguments.count > 1 else {
    print("Usage: extract_pdf <input.pdf> [output_img_dir]")
    exit(1)
}

let pdfPath = CommandLine.arguments[1]
let pdfURL = URL(fileURLWithPath: pdfPath)
guard let doc = PDFDocument(url: pdfURL) else {
    print("Error: Could not open PDF at \(pdfPath)")
    exit(1)
}

let baseName = pdfURL.deletingPathExtension().lastPathComponent
let outDir: URL
if CommandLine.arguments.count > 2 {
    outDir = URL(fileURLWithPath: CommandLine.arguments[2])
} else {
    outDir = URL(fileURLWithPath: "output/images/\(baseName)")
}

try? FileManager.default.createDirectory(at: outDir, withIntermediateDirectories: true, attributes: nil)

var flowLines: [String] = []

let totalPages = doc.pageCount
print("--- Processing \(totalPages) pages from \(pdfPath) ---")

for i in 0..<totalPages {
    guard let page = doc.page(at: i) else { continue }
    let pageNum = i + 1
    let imgName = "page_\(pageNum).png"
    let imgURL = outDir.appendingPathComponent(imgName)
    
    // 1. Render page to high-res image
    let bounds = page.bounds(for: .mediaBox)
    let scale: CGFloat = 2.0 // High DPI (Retina)
    let width = Int(bounds.width * scale)
    let height = Int(bounds.height * scale)
    
    let colorSpace = CGColorSpaceCreateDeviceRGB()
    let bitmapInfo = CGImageAlphaInfo.premultipliedLast.rawValue
    if let ctx = CGContext(data: nil, width: width, height: height, bitsPerComponent: 8, bytesPerRow: 0, space: colorSpace, bitmapInfo: bitmapInfo) {
        ctx.setFillColor(CGColor(red: 1, green: 1, blue: 1, alpha: 1))
        ctx.fill(CGRect(x: 0, y: 0, width: width, height: height))
        ctx.saveGState()
        ctx.scaleBy(x: scale, y: scale)
        page.draw(with: .mediaBox, to: ctx)
        ctx.restoreGState()
        
        if let cgImg = ctx.makeImage(), let dest = CGImageDestinationCreateWithURL(imgURL as CFURL, kUTTypePNG, 1, nil) {
            CGImageDestinationAddImage(dest, cgImg, nil)
            CGImageDestinationFinalize(dest)
        }
    }
    
    // 2. Extract text and record interleaved marker
    flowLines.append("[IMG: \(imgName)]")
    if let text = page.string?.trimmingCharacters(in: .whitespacesAndNewlines), !text.isEmpty {
        flowLines.append(text)
    }
}

let flowFile = outDir.appendingPathComponent("document_flow.txt")
let fullFlow = flowLines.joined(separator: "\n\n")
try? fullFlow.write(to: flowFile, atomically: true, encoding: .utf8)

print("--- Extracted \(totalPages) page images to '\(outDir.path)' ---")
print("--- Dual-track interleaved flow saved to '\(flowFile.path)' ---")
