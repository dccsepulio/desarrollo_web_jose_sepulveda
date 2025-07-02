package desarrollo_web.jose_sepulveda.tarea4.models;

import java.time.LocalDateTime;

import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.SequenceGenerator;
import jakarta.persistence.Table;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;

@Entity 
@Table(name = "nota")
public class Note {
    @Id
    @SequenceGenerator(
        name = "nota_sequence",
        sequenceName = "nota_sequence",
        allocationSize = 1
    )
    @GeneratedValue(
        strategy = GenerationType.SEQUENCE,
        generator = "nota_sequence"
    )
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "actividad_id")
    private Activity activity;

    @Min(1) 
    @Max(7)
    private Integer valor;

    private LocalDateTime createdAt = LocalDateTime.now();

    public Long getId() {
        return id;
    }

    public Integer getValor() { 
        return this.valor; 
    }

    public LocalDateTime getFechaInicio() {
        return createdAt;
    }

    public void setId(Long id) { 
        this.id = id; 
    }

    public void setValor(Integer valor2) {
        this.valor = valor2; 
    }

    public void setActivity(Activity act) {
        this.activity = act;
    }
}
