from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from infrastructure.db.mysql import mysql_conn
from .movies_schemas import MovieCreateIn, MovieUpdateIn, MovieOut
from ..admins.auth.admin_auth_deps import require_admin

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("", response_model=list[MovieOut])
def get_all_movies(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    genre: Optional[str] = None,
    _admin: dict = Depends(require_admin)
):
    with mysql_conn() as conn:
        with conn.cursor() as cur:
            if genre:
                cur.execute(
                    "SELECT movie_id, title, director, year, genre, rating, duration, is_active, created_at "
                    "FROM movies WHERE genre = %s AND is_active = 1 "
                    "ORDER BY movie_id DESC LIMIT %s OFFSET %s",
                    (genre, limit, offset)
                )
            else:
                cur.execute(
                    "SELECT movie_id, title, director, year, genre, rating, duration, is_active, created_at "
                    "FROM movies WHERE is_active = 1 "
                    "ORDER BY movie_id DESC LIMIT %s OFFSET %s",
                    (limit, offset)
                )
            rows = cur.fetchall()

            movies = []
            for row in rows:
                movies.append(MovieOut(
                    movie_id=row[0],
                    title=row[1],
                    director=row[2],
                    year=row[3],
                    genre=row[4],
                    rating=float(row[5]) if row[5] else 0,
                    duration=row[6],
                    is_active=bool(row[7]),
                    created_at=row[8]
                ))
            return movies


@router.get("/{movie_id}", response_model=MovieOut)
def get_movie_by_id(
    movie_id: int,
    _admin: dict = Depends(require_admin)
):
    with mysql_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT movie_id, title, director, year, genre, rating, duration, is_active, created_at "
                "FROM movies WHERE movie_id = %s AND is_active = 1",
                (movie_id,)
            )
            row = cur.fetchone()

            if not row:
                raise HTTPException(status_code=404, detail="Movie not found")

            return MovieOut(
                movie_id=row[0],
                title=row[1],
                director=row[2],
                year=row[3],
                genre=row[4],
                rating=float(row[5]) if row[5] else 0,
                duration=row[6],
                is_active=bool(row[7]),
                created_at=row[8]
            )


@router.post("", response_model=MovieOut)
def create_movie(
    data: MovieCreateIn,
    _admin: dict = Depends(require_admin)
):
    with mysql_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO movies (title, director, year, genre, rating, duration, is_active) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (data.title, data.director, data.year, data.genre, data.rating, data.duration, data.is_active)
            )
            conn.commit()
            movie_id = cur.lastrowid

            cur.execute(
                "SELECT movie_id, title, director, year, genre, rating, duration, is_active, created_at "
                "FROM movies WHERE movie_id = %s",
                (movie_id,)
            )
            row = cur.fetchone()

            return MovieOut(
                movie_id=row[0],
                title=row[1],
                director=row[2],
                year=row[3],
                genre=row[4],
                rating=float(row[5]) if row[5] else 0,
                duration=row[6],
                is_active=bool(row[7]),
                created_at=row[8]
            )


@router.patch("/{movie_id}", response_model=MovieOut)
def update_movie(
    movie_id: int,
    data: MovieUpdateIn,
    _admin: dict = Depends(require_admin)
):
    updates = []
    values = []

    if data.title is not None:
        updates.append("title = %s")
        values.append(data.title)
    if data.director is not None:
        updates.append("director = %s")
        values.append(data.director)
    if data.year is not None:
        updates.append("year = %s")
        values.append(data.year)
    if data.genre is not None:
        updates.append("genre = %s")
        values.append(data.genre)
    if data.rating is not None:
        updates.append("rating = %s")
        values.append(data.rating)
    if data.duration is not None:
        updates.append("duration = %s")
        values.append(data.duration)
    if data.is_active is not None:
        updates.append("is_active = %s")
        values.append(1 if data.is_active else 0)

    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    values.append(movie_id)

    with mysql_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM movies WHERE movie_id = %s", (movie_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Movie not found")

            cur.execute(
                f"UPDATE movies SET {', '.join(updates)} WHERE movie_id = %s",
                tuple(values)
            )
            conn.commit()

            cur.execute(
                "SELECT movie_id, title, director, year, genre, rating, duration, is_active, created_at "
                "FROM movies WHERE movie_id = %s",
                (movie_id,)
            )
            row = cur.fetchone()

            return MovieOut(
                movie_id=row[0],
                title=row[1],
                director=row[2],
                year=row[3],
                genre=row[4],
                rating=float(row[5]) if row[5] else 0,
                duration=row[6],
                is_active=bool(row[7]),
                created_at=row[8]
            )


@router.delete("/{movie_id}")
def delete_movie(
    movie_id: int,
    hard: bool = Query(False),
    _admin: dict = Depends(require_admin)
):
    with mysql_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM movies WHERE movie_id = %s", (movie_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Movie not found")

            if hard:
                cur.execute("DELETE FROM movies WHERE movie_id = %s", (movie_id,))
                conn.commit()
                return {"ok": True, "hard": True, "message": "Movie permanently deleted"}
            else:
                cur.execute("UPDATE movies SET is_active = 0 WHERE movie_id = %s", (movie_id,))
                conn.commit()
                return {"ok": True, "hard": False, "message": "Movie deactivated"}