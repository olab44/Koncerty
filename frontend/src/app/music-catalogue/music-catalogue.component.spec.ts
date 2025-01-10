import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MusicCatalogueComponent } from './music-catalogue.component';

describe('MusicCatalogueComponent', () => {
  let component: MusicCatalogueComponent;
  let fixture: ComponentFixture<MusicCatalogueComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MusicCatalogueComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MusicCatalogueComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
